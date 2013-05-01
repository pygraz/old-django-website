from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = patterns(
    '',
    url('^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})$',
        views.DetailView.as_view(), name="view-meetup"),
    url('^(?P<pk>\d+)/$',
        views.DetailView.as_view(), name="meetup-permalink"),
    url('^sessions/submit/$',
        views.SubmitSession.as_view(), name="submit-session"),
    url('^sessions/(?P<pk>\d+)/$',
        views.ViewSession.as_view(), name="view-session"),
    url('^sessions/(?P<pk>\d+)/edit/$',
        login_required(views.EditSession.as_view()), name="edit-session"),
    url('^sessions/(?P<pk>\d+)/delete/$',
        login_required(views.DeleteSession.as_view()), name="delete-session"),
    url('^ical/$', views.ICalendarView.as_view(), name="ical"),
)
