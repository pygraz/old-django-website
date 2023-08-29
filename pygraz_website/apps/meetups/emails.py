from django.contrib.sites.models import Site
from django.core.mail import mail_admins
from django.template.loader import render_to_string

__ALL__ = ["notify_admins_for_new_session"]


def notify_admins_for_new_session(session):
    current_site = Site.objects.get_current()
    mail_admins(
        "Neue Session eingetragen",
        render_to_string(
            "meetups/emails/new_session.txt",
            {
                "session": session,
                "session_url": f"https://{current_site.domain}{session.get_absolute_url()}",
            },
        ),
        fail_silently=False,
    )
