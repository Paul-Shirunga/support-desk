from django.core.management.base import BaseCommand
from tickets.email_to_ticket import create_ticket_from_latest_email


class Command(BaseCommand):
    help = "Fetch latest emails and create tickets"

    def handle(self, *args, **options):
        self.stdout.write("📥 Fetching emails...")

        ticket = create_ticket_from_latest_email()

        if ticket:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Ticket #{ticket.id} created from email")
            )
        else:
            self.stdout.write(
                self.style.WARNING("⚠️ No new emails to process")
            )
