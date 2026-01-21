import imaplib
import email
from email.header import decode_header

from tickets.models import Ticket


def create_ticket_from_latest_email():
    """
    Fetch the latest unread email and create a ticket.
    """

    IMAP_SERVER = "outlook.office365.com"
    EMAIL_ACCOUNT = "support@yourdomain.com"   # CHANGE THIS
    EMAIL_PASSWORD = "YOUR_PASSWORD"           # CHANGE THIS

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        if not email_ids:
            print("📭 No new emails")
            return None

        latest_email_id = email_ids[-1]
        _, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = msg_data[0][1]

        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg.get("Subject"))[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        from_email = email.utils.parseaddr(msg.get("From"))[1]

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        ticket = Ticket.objects.create(
            title=subject or "No subject",
            description=body[:5000],
            sender=from_email,
            source="email",
            status="open",
        )

        mail.store(latest_email_id, "+FLAGS", "\\Seen")
        mail.logout()

        print(f"✅ Ticket #{ticket.id} created from email")
        return ticket

    except Exception as e:
        print("❌ Email fetch failed:", e)
        return None
