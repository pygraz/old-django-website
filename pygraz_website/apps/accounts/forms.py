from userena import forms as userena_forms
from django.contrib.auth import forms as auth_forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Submit, Field, Layout

from django.utils.translation import gettext_lazy as _


class AuthenticationForm(userena_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("identification", autofocus="autofocus"),
            Field("password"),
            Field("remember_me"),
            ButtonHolder(Submit("login", _("Log in"))),
        )


class ChangeEmailForm(userena_forms.ChangeEmailForm):
    def __init__(self, *args, **kwargs):
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("email", autofocus="autofocus"),
            ButtonHolder(Submit("save", _("Save changes"))),
        )


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("old_password", autofocus="autofocus"),
            Field("new_password1"),
            Field("new_password2"),
            ButtonHolder(Submit("save", _("Save changes"))),
        )


class PasswordResetForm(auth_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("email", autofocus="autofocus"),
            ButtonHolder(Submit("save", _("Reset password"))),
        )


class SetPasswordForm(auth_forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("new_password1", autofocus="autofocus"),
            Field("new_password2"),
            ButtonHolder(Submit("save", _("Reset password"))),
        )


class EditProfileForm(userena_forms.EditProfileForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("first_name", autofocus="autofocus"),
            Field("last_name"),
            Field("mugshot"),
            Field("privacy"),
            ButtonHolder(Submit("save", _("Save changes"))),
        )


class SignupForm(userena_forms.SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("username"),
            Field("email"),
            Field("password1"),
            Field("password2"),
            ButtonHolder(Submit("register", _("Registrieren"))),
        )
