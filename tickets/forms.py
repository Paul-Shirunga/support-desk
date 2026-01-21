from django import forms
from .models import Ticket

class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["status", "priority", "resolution"]
        widgets = {
            "resolution": forms.Textarea(attrs={"rows": 4}),
        }
