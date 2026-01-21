from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket


def ticket_list(request):
    tickets = Ticket.objects.all().order_by("-id")

    context = {
        "tickets": tickets,
        "sidebar": True,

        "open_count": Ticket.objects.filter(status="open").count(),
        "investigation_count": Ticket.objects.filter(status="under_investigation").count(),
        "on_hold_count": Ticket.objects.filter(status="on_hold").count(),
        "in_progress_count": Ticket.objects.filter(status="in_progress").count(),
        "closed_count": Ticket.objects.filter(status="closed").count(),
    }

    return render(request, "tickets/ticket_list.html", context)


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, "tickets/ticket_detail.html", {
        "ticket": ticket,
        "sidebar": True,
    })


def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in dict(Ticket.STATUS_CHOICES):
            ticket.status = new_status
            ticket.save()

    return redirect("tickets:ticket_list")
