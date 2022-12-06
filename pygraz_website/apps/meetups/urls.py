from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path(
        "<int:year>-<int:month>-<int:day>/",
        views.DetailView.as_view(),
        name="view-meetup",
    ),
    path("<int:pk>/", views.DetailView.as_view(), name="meetup-permalink"),
    path("sessions/submit/", views.SubmitSession.as_view(), name="submit-session"),
    path("sessions/<int:pk>/", views.ViewSession.as_view(), name="view-session"),
    path(
        "sessions/<int:pk>/edit/",
        login_required(views.EditSession.as_view()),
        name="edit-session",
    ),
    path(
        "sessions/<int:pk>/delete/",
        login_required(views.DeleteSession.as_view()),
        name="delete-session",
    ),
    path("ical/", views.ICalendarView.as_view(), name="ical"),
]
