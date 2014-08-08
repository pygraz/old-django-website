#-*- encoding: utf-8 -*-
import datetime
import pytz
import urlparse
import collections
import icalendar

from django.views import generic as generic_views
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django.conf import settings

from . import models
from . import forms
from . import emails
from .decorators import allow_only_staff_or_author_during_submission


RSVPCollection = collections.namedtuple('RSVPCollection',
                                        'coming maybe not_coming')


class NextRedirectMixin(object):
    """
    A simple mixin for checking for a next parameter for redirects.
    """
    redirect_param = 'next'

    def get_next_redirect(self):
        next = self.request.GET.get(self.redirect_param)
        if next is None:
            return None
        netloc = urlparse.urlparse(next)[1]
        if netloc is None or netloc == "" or netloc == self.request.get_host():
            return next
        return None

    def get_success_url(self):
        next = self.get_next_redirect()
        if next:
            return next
        return super(NextRedirectMixin, self).get_success_url()


class DetailView(generic_views.DetailView):
    """
    Shows the details of a single meetup. There are two entry points: Via the
    PK of the meetup and via its date.

    If neither criteria match a meetup, a 404 error page is shown.
    """
    model = models.Meetup

    def get_object(self):
        if 'pk' in self.kwargs:
            return get_object_or_404(
                self.model.objects.select_related('location'),
                pk=self.kwargs.get('pk'))
        else:
            date_start = datetime.datetime(
                int(self.kwargs.get('year')),
                int(self.kwargs.get('month')),
                int(self.kwargs.get('day')), 0, 0, 0)
            date_end = date_start + datetime.timedelta(days=1)
            local_tz = timezone.get_default_timezone()
            date_start = local_tz.localize(date_start)
            date_end = local_tz.localize(date_end)
            utc_date_start = date_start.astimezone(pytz.utc)
            utc_date_end = date_end.astimezone(pytz.utc)
            result = self.model.objects.filter(
                start_date__gte=utc_date_start,
                start_date__lte=utc_date_end).select_related('location')
            if not len(result):
                raise Http404
            return result[0]

    def get_context_data(self, *args, **kwargs):
        data = super(DetailView, self).get_context_data(*args, **kwargs)
        data['rsvps'] = self._get_rsvps()
        return data

    def _get_rsvps(self):
        result = RSVPCollection([], [], [])
        for rsvp in self.object.rsvps.all():
            if rsvp.status:
                getattr(result, rsvp.status).append(rsvp)
        return result


class SubmitSession(NextRedirectMixin, generic_views.CreateView):
    """
    Allows a user or guest to submit a session.
    """
    model = models.Session

    def get_form_class(self):
        return forms.get_session_submission_form_class(self.request)

    def form_valid(self, form):
        session = form.save(commit=False)
        if self.request.user.is_authenticated():
            session.speaker = self.request.user
        session.save()
        emails.notify_admins_for_new_session(session)
        messages.success(self.request, "Session erstellt.")
        return HttpResponseRedirect(self.get_success_url())


class ViewSession(generic_views.DetailView):
    """
    Shows a single session by its PK and returns a 404 page if no matching
    session could be found.
    """
    model = models.Session

    def get_context_data(self, **kwargs):
        data = super(ViewSession, self).get_context_data(**kwargs)
        can_delete = self.request.user.is_superuser or\
            self.request.user.is_staff or\
            (self.object.speaker and self.object.speaker == self.request.user)
        data.update({
            'can_delete': can_delete,
            'can_edit': can_delete,
        })
        return data

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])


class EditSession(generic_views.UpdateView):
    """
    During the submission period, the author as well as staff members can edit
    the session. Once it has been attached to a meetup, only staff members can
    edit the proposal anymore.
    """
    model = models.Session
    form_class = forms.EditSessionForm

    @allow_only_staff_or_author_during_submission
    def dispatch(self, request, *args, **kwargs):
        return super(EditSession, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        if hasattr(self, 'object') and self.object:
            return self.object
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def form_valid(self, form):
        messages.success(self.request, "Session aktualisiert.")
        return super(EditSession, self).form_valid(form)


class DeleteSession(NextRedirectMixin, generic_views.DeleteView):
    """
    During the submission period, author and staff can delete a session.
    Afterwards only the staff.
    """
    model = models.Session
    success_url = '/'

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        data = super(DeleteSession, self).get_context_data(**kwargs)
        data.update({
            'cancel_url': self.get_success_url()
        })
        return data

    def delete(self, request, *args, **kwargs):
        response = super(DeleteSession, self).delete(request, *args, **kwargs)
        messages.success(request, "Session gelöscht.")
        return response

    @allow_only_staff_or_author_during_submission
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteSession, self).dispatch(request, *args, **kwargs)


class ICalendarView(generic_views.View):
    """
    This offers a simple ical rendering of all the meetups.
    """
    def get_meetup_summary(self, meetup):
        return "PyGRAZ-Meetup am {0}".format(meetup.start_date.date())

    def get_meetup_description(self, meetup):
        return """Details: https://{0}{1}""".format(
            Site.objects.get_current().domain, meetup.get_absolute_url())

    def get(self, request, *args, **kwargs):
        cal = icalendar.Calendar()
        cal.add('X-WR-CALNAME', settings.MEETUPS_CALENDAR_NAME)
        site = Site.objects.get_current()
        for meetup in models.Meetup.objects.all():
            evt = icalendar.Event()
            evt.add('summary', self.get_meetup_summary(meetup))
            evt.add('description', self.get_meetup_description(meetup))
            evt.add('dtstart', meetup.start_date)
            evt['uid'] = '{0}/meetups/{1}'.format(site.domain, meetup.pk)
            cal.add_component(evt)
        response = HttpResponse(cal.to_ical(), content_type='text/calendar')
        response['Content-Disposition'] = 'attachment;filename=pygraz.ics'
        return response

