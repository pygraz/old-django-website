from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Fieldset, Layout, Submit
from django import forms

from . import models


class CompanySubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    class Meta:
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
