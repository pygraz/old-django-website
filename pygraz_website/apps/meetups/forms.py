# -*- encoding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit

from captcha.fields import ReCaptchaField

from . import models


class AnonymousSessionSubmissionForm(forms.ModelForm):
    speaker_name = forms.CharField(required=True, label="Dein Name")
    speaker_email = forms.EmailField(required=True, label="Deine E-Mail-Adresse")
    captcha = ReCaptchaField(attrs={'theme': 'clean'})

    class Meta(object):
        model = models.Session
        fields = ('title', 'abstract', 'speaker_name', 'speaker_email')

    def __init__(self, *args, **kwargs):
        super(AnonymousSessionSubmissionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        layout = Layout(
            Field('title'), Field('abstract'),
            Field('speaker_name'), Field('speaker_email'),
            Field('captcha'),
            ButtonHolder(Submit("submit", "Abschicken"))
        )
        self.helper.add_layout(layout)
        self.fields['speaker_email'].help_text = u"""Wir benötigen deine E-Mail-Adresse, um etwaige Termin und Themefragen mit dir abklären zu können."""


class RegisteredSessionSubmissionForm(forms.ModelForm):
    class Meta(object):
        model = models.Session
        fields = ('title', 'abstract',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        layout = Layout(
            Field('title'), Field('abstract'),
            ButtonHolder(Submit("submit", "Abschicken"))
        )
        self.helper.add_layout(layout)
        super(RegisteredSessionSubmissionForm, self).__init__(*args, **kwargs)


class EditSessionForm(forms.ModelForm):
    class Meta(object):
        model = models.Session
        fields = ('title', 'abstract', 'slides_url', 'notes')

    def __init__(self, *args, **kwargs):
        super(EditSessionForm, self).__init__(*args, **kwargs)
        self.fields['abstract'].help_text = u"""Bitte beschreibe kurz, worum es in deiner Session geht. Wo sind die Einsatzgebiete, wie komplex ist das Ganze usw."""
        self.helper = FormHelper()
        layout = Layout(
            Field('title', autofocus='autofocus'), Field('abstract'),
            Field('slides_url'), Field('notes'),
            ButtonHolder(Submit('submit', u'Änderungen speichern'))
            )
        self.helper.add_layout(layout)


def get_session_submission_form_class(request):
    if request.user.is_authenticated():
        return RegisteredSessionSubmissionForm
    return AnonymousSessionSubmissionForm
