from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home_redirect(request):
    return redirect("tickets:ticket_list")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("tickets/", include("tickets.urls")),
    path("", home_redirect),  # 👈 ROOT FIX
]
