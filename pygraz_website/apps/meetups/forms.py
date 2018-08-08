# -*- encoding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit

from captcha.fields import ReCaptchaField

from . import models


class AnonymousSessionSubmissionForm(forms.ModelForm):
    speaker_name = forms.CharField(required=True, label="Dein Name")
    speaker_email = forms.EmailField(required=True, label="Deine E-Mail-Adresse")
    captcha = ReCaptchaField(attrs={'theme': 'white'})

    class Meta(object):
        model = models.Session
        fields = ('title', 'abstract', 'speaker_name', 'speaker_email', 'type')
        widgets = {
            'type': forms.RadioSelect
        }
        help_texts = {
            'speaker_email': u"""Wir benötigen deine E-Mail-Adresse, um etwaige Termin und Themefragen mit dir abklären zu können."""
        }

    def __init__(self, *args, **kwargs):
        super(AnonymousSessionSubmissionForm, self).__init__(*args, **kwargs)
        del self.fields['abstract'].widget.attrs['cols']
        self.fields['type'].required = True
        self.fields['type'].empty_label = None
        _extend_type_choice_labels(self.fields['type'])
        self.helper = FormHelper()
        layout = Layout(
            Field('title'), Field('abstract'),
            Field('speaker_name'), Field('speaker_email'),
            Field('captcha'),
            Field('type'),
            ButtonHolder(Submit("submit", "Abschicken"))
        )
        self.helper.add_layout(layout)


class RegisteredSessionSubmissionForm(forms.ModelForm):
    class Meta(object):
        model = models.Session
        fields = ('title', 'abstract', 'type',)
        widgets = {
            'type': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super(RegisteredSessionSubmissionForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = True
        self.fields['type'].empty_label = None
        _extend_type_choice_labels(self.fields['type'])
        self.helper = FormHelper()
        layout = Layout(
            Field('title'), Field('abstract'), Field('type'),
            ButtonHolder(Submit("submit", "Abschicken"))
        )
        self.helper.add_layout(layout)


class EditSessionForm(forms.ModelForm):
    class Meta(object):
        model = models.Session
        fields = ('title', 'abstract', 'slides_url', 'notes', 'type')
        widgets = {
            'type': forms.RadioSelect
        }
        help_texts = {
            'abstract': u"""Bitte beschreibe kurz, worum es in deiner Session geht. Wo sind die Einsatzgebiete, wie komplex ist das Ganze usw."""
        }

    def __init__(self, *args, **kwargs):
        super(EditSessionForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = True
        self.fields['type'].empty_label = None
        _extend_type_choice_labels(self.fields['type'])
        self.helper = FormHelper()
        layout = Layout(
            Field('title', autofocus='autofocus'), Field('abstract'),
            Field('type'), Field('slides_url'), Field('notes'),
            ButtonHolder(Submit('submit', u'Änderungen speichern'))
            )
        self.helper.add_layout(layout)


def _extend_type_choice_labels(field):
    types = dict([(type_.pk, type_) for type_ in field.queryset.all()])
    new_choices = []
    for choice in field.choices:
        if choice[0] != u"":
            new_choices.append((choice[0], mark_safe(u"{0}: <span>{1}</span>".format(choice[1], types[choice[0]].description))))
        else:
            new_choices.append(choice)
    field.choices = new_choices


def get_session_submission_form_class(request):
    if request.user.is_authenticated():
        return RegisteredSessionSubmissionForm
    return AnonymousSessionSubmissionForm
