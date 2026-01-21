import email
import imaplib
import os
from django.conf import settings
from django.utils import timezone
from django.core.files.base import ContentFile

from tickets.models import Ticket, TicketAttachment


def fetch_email_tickets():
    print("Connecting to mailbox...")

    mail = imaplib.IMAP4_SSL(settings.EMAIL_HOST_IMAP)
    mail.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
    mail.select(settings.EMAIL_FOLDER)

    status, messages = mail.search(None, "UNSEEN")   # unread emails only
    email_ids = messages[0].split()

    print(f"Unread emails found: {len(email_ids)}")

    for msg_id in email_ids:
        status, msg_data = mail.fetch(msg_id, "(RFC822)")
        raw_email = msg_data[0][1]

        msg = email.message_from_bytes(raw_email)

        sender = email.utils.parseaddr(msg.get("From"))[1]
        subject = msg.get("Subject", "(No Subject)")
        message_id = msg.get("Message-ID", "")

        # Prevent duplicate ticket creation
        if Ticket.objects.filter(raw_message_id=message_id).exists():
            print("Duplicate email ignored.")
            continue

        # Extract body
        body = "(No content)"
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        # Create ticket
        ticket = Ticket.objects.create(
            title=subject,
            description=body,
            sender=sender,
            source="email",
            raw_message_id=message_id,
        )

        print(f"Created Ticket #{ticket.id} from {sender}")

        # ---------------------------------------
        # PROCESS ATTACHMENTS
        # ---------------------------------------
        for part in msg.walk():
            if part.get_filename():
                filename = part.get_filename()
                payload = part.get_payload(decode=True)

                attachment = TicketAttachment(
                    ticket=ticket,
                    filename=filename,
                    content_type=part.get_content_type(),
                )
                attachment.file.save(filename, ContentFile(payload))
                attachment.save()

                print(f"Saved attachment: {filename}")

        # Mark email as read
        mail.store(msg_id, "+FLAGS", "\\Seen")

    mail.close()
    mail.logout()

    print("Email fetch complete.")
