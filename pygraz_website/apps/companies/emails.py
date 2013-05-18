from django.core.mail import mail_admins
from django.template.loader import render_to_string


def notify_admins_for_approval(company):
    mail_admins("Neue Firma", render_to_string('companies/emails/admin_approval.txt', {
        'company': company
        }))
