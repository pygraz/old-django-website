from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

# from userena import settngs as userena_settings
from userena import views as userena_views

from . import forms
from . import views


def merge_dicts(a, b):
    result = {}
    result.update(a)
    result.update(b)
    return result


urlpatterns = [
    url(r'^signin/$',
        userena_views.signin,
        {'auth_form': forms.AuthenticationForm},
        name='userena_signin'),
    url(r'^signup/$',
        userena_views.signup,
        {'signup_form': forms.SignupForm},
        name='userena_signup'),
    url(r'^(?P<username>[\.\w]+)/email/$',
        userena_views.email_change,
        {'email_form': forms.ChangeEmailForm},
        name='userena_email_change'),
    url(r'^(?P<username>[\.\w]+)/password/$',
        userena_views.password_change,
        {'pass_form': forms.PasswordChangeForm},
        name='userena_password_change'),
    url(r'^password/reset/$',
        auth_views.PasswordResetView,
        merge_dicts(
            {
                'template_name': 'userena/password_reset_form.html',
                'email_template_name': 'userena/emails/password_reset_message.txt',
                'password_reset_form': forms.PasswordResetForm,
                'extra_context': {'without_usernames': False}
            },
            { 'post_reset_redirect': 'userena_password_reset_done' }
        ),
        name='userena_password_reset'),
    url(r'^password/reset/confirm/(?P<%s>[0-9A-Za-z]+)-(?P<token>.+)/$' % 'uidb64',
        auth_views.PasswordResetConfirmView,
        merge_dicts(
            {
                'template_name': 'userena/password_reset_confirm_form.html',
                'set_password_form': forms.SetPasswordForm,
            },
            {'post_reset_redirect': 'userena_password_reset_complete'}
        ),
        name='userena_password_reset_confirm'),
    url(r'^(?P<username>[\.\w]+)/edit/$',
        userena_views.profile_edit,
        {'edit_profile_form': forms.EditProfileForm},
        name='userena_profile_edit'),
    url(r'^(?P<username>[\.\w]+)/contents/$',
        login_required(views.MyContentsView.as_view()),
        name='my_contents'),
]
