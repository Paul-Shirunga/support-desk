from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tickets.models import UserProfile

class Command(BaseCommand):
    help = "Sync users from Azure AD"

    def handle(self, *args, **kwargs):
        users = get_azure_users()  # ← your existing Azure fetch

        for u in users:
            email = u.get("mail") or u.get("userPrincipalName")
            display_name = u.get("displayName") or email.split("@")[0]

            user, _ = User.objects.get_or_create(
                username=email,
                defaults={"email": email}
            )

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.display_name = display_name
            profile.email = email
            profile.save()

        self.stdout.write(self.style.SUCCESS("Azure users synced"))
