from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from core.models import Meetup


def home_view(request: HttpRequest):
    return render(
        request,
        "core/home.html",
        {"next_meetup": Meetup.objects.next_meetup(), "past_meetups": Meetup.objects.past_meetups()},
    )


def meetup_view(request: HttpRequest, pk: int):
    meetup = get_object_or_404(Meetup, pk=pk)
    return render(request, "core/meetup.html", {"meetup": meetup})
