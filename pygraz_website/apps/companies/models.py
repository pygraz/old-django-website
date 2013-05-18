# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from pygraz_website.apps.accounts import contents


COUNTRY_CHOICES = (
    ('AT', u'Österreich'),
)


class Company(models.Model):
    name = models.CharField("Name", max_length=100)
    website = models.URLField("Webseite")
    contact_email = models.EmailField("E-Mail-Kontakt", blank=True)
    description = models.TextField("Beschreibung", blank=True)

    address_line = models.CharField("Addresse", max_length=255)
    postal_code = models.CharField("Postleitzahl", max_length=10)
    city = models.CharField("Stadt", max_length=50)
    country = models.CharField("Land", max_length=3,
                               choices=COUNTRY_CHOICES)

    approved = models.BooleanField("verifiziert", default=False)
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True,
                                     blank=True,
                                     related_name='companies')

    pub_date = models.DateTimeField("Erstellt am", auto_now_add=True)

    def get_absolute_url(self):
        return reverse('company-details', kwargs={'pk': self.pk})

    class Meta(object):
        verbose_name = _("company")
        verbose_name_plural = _("companies")
        ordering = ('name',)


class CompanyContentProxy(contents.BaseProxy):
    model_class = Company
    label = "Meine Firmen"

    def get_queryset(self):
        return self.request.user.companies.all()

contents.register(CompanyContentProxy)