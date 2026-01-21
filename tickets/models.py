from django.utils import timezone
from datetime import timedelta



from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ====================================================
# USER PROFILE (FOR AD / DISPLAY NAME)
# ====================================================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.display_name or self.user.username


# ====================================================
# REQUIRED FOR OLD MIGRATIONS (DO NOT REMOVE)
# ====================================================
def attachment_upload_to(instance, filename):
    return f"ticket_attachments/ticket_{instance.ticket.id}/{filename}"


# ====================================================
# TICKET MODEL
# ====================================================
class Ticket(models.Model):

    # =========================
    # STATUS CHOICES
    # =========================
    STATUS_CHOICES = [
        ("open", "Open"),
        ("under_investigation", "Under Investigation"),
        ("on_hold", "On Hold"),
        ("in_progress", "In Progress"),
        ("closed", "Closed"),
    ]

    # =========================
    # PRIORITY CHOICES
    # =========================
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    # =========================
    # CORE FIELDS
    # =========================
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="open",
        db_index=True
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
        db_index=True
    )

    # =========================
    # USERS
    # =========================
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_tickets"
    )

    assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_tickets"
    )

    # =========================
    # RESOLUTION
    # =========================
    resolution = models.TextField(blank=True)

    # =========================
    # TIMESTAMPS
    # =========================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    # =========================
    # EMAIL SUPPORT
    # =========================
    sender = models.EmailField(blank=True)
    source = models.CharField(max_length=30, default="web")

    # ====================================================
    # # =========================
# SLA LOGIC
# =========================
def sla_due_at(self):
    """Return SLA deadline datetime"""
    sla_hours = {
        "low": 72,
        "medium": 48,
        "high": 24,
        "urgent": 4,
    }
    hours = sla_hours.get(self.priority, 48)
    return self.created_at + timedelta(hours=hours)


def sla_remaining(self):
    """Return remaining SLA time"""
    return self.sla_due_at() - timezone.now()


def is_overdue(self):
    """Check if SLA is breached"""
    return timezone.now() > self.sla_due_at()


    # =========================
    # HELPERS
    # =========================
    def mark_resolved(self):
        self.status = "closed"
        self.resolved_at = timezone.now()
        self.save(update_fields=["status", "resolved_at", "updated_at"])

    def __str__(self):
        return f"[#{self.id}] {self.title}"


# ====================================================
# ATTACHMENTS (REQUIRED BY MIGRATIONS)
# ====================================================
class TicketAttachment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        related_name="attachments",
        on_delete=models.CASCADE
    )

    file = models.FileField(upload_to=attachment_upload_to)
    filename = models.CharField(max_length=255, blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    size = models.PositiveIntegerField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file and not self.filename:
            self.filename = self.file.name
        if self.file:
            self.size = self.file.size
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.filename} (ticket #{self.ticket.id})"
