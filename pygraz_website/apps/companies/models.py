# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from pygraz_website.apps.accounts import contents
import guardian.shortcuts


COUNTRY_CHOICES = (
    ('AT', _('Austria')),
)


class Company(models.Model):
    name = models.CharField(_("name"), max_length=100)
    website = models.URLField(_("website"))
    contact_email = models.EmailField(_("contact e-mail"), blank=True)
    description = models.TextField(_("description"), blank=True)

    address_line = models.CharField(_("address line"), max_length=255)
    postal_code = models.CharField(_("postal code"), max_length=10)
    city = models.CharField(_("city"), max_length=50)
    country = models.CharField(_("country"), max_length=3,
                               choices=COUNTRY_CHOICES)

    approved = models.BooleanField(_("approved"), default=False)
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     blank=True,
                                     related_name='companies')

    pub_date = models.DateTimeField(_("Published at"), auto_now_add=True)

    def get_absolute_url(self):
        return reverse('company-details', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = _("company")
        verbose_name_plural = _("companies")
        ordering = ('name',)


class CompanyContentProxy(contents.BaseProxy):
    model_class = Company
    label = _("My companies")

    def get_queryset(self):
        return guardian.shortcuts.get_objects_for_user(self.request.user, 'companies.change_company')

contents.register(CompanyContentProxy)
