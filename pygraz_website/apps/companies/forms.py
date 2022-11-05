# -*- encoding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, Fieldset

from . import models


class CompanySubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompanySubmissionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        layout = Layout(
            Fieldset("Über Ihre Firma", "name", "description"),
            Fieldset(
                "Kontaktdaten",
                "contact_email",
                "website",
                "address_line",
                "postal_code",
                "city",
                "country",
            ),
            ButtonHolder(Submit("submit", "Abschicken")),
        )
        self.helper.add_layout(layout)

    class Meta(object):
        model = models.Company
        fields = (
            "name",
            "description",
            "contact_email",
            "website",
            "address_line",
            "postal_code",
            "city",
            "country",
        )
