from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _
from userena.models import UserenaBaseProfile


class Profile(UserenaBaseProfile):
    user = models.OneToOneField(
        auth_models.User,
        unique=True,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="profile",
    )

    def __str__(self):
        return self.user.username
