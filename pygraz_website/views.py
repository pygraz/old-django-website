from django.shortcuts import render
from django.utils.timezone import now
from django.core.urlresolvers import reverse

from .apps.meetups import models as meetup_models
from .apps.meetups import forms as meetup_forms


def index(request):
    """
    Frontpage view listing all session proposals, past meetups and the next meetup.
    """
    today = now()
    try:
        next_meetup = meetup_models.Meetup.objects.get_future_meetups(now=today)\
            .order_by('-start_date')\
            .prefetch_related('sessions', 'sessions__speaker')\
            .select_related('location')[0]
    except:
        next_meetup = None
    past_meetups = meetup_models.Meetup.objects.get_past_meetups(now=today)
    session_proposals = meetup_models.Session.objects.get_proposals().select_related('speaker')
    submission_form = meetup_forms.get_session_submission_form_class(request)()
    submission_form.helper.set_form_action(reverse('submit-session') + '?next=/')
    return render(request, 'index.html', {
        'next_meetup': next_meetup,
        'past_meetups': past_meetups,
        'session_proposals': session_proposals,
        'submission_form': submission_form,
        })
