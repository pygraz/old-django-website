from django.urls import path

from core import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("meetup/<int:pk>/", views.meetup_view, name="meetup"),
]
