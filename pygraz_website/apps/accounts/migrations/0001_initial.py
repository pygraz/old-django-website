import easy_thumbnails.fields
import userena.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "mugshot",
                    easy_thumbnails.fields.ThumbnailerImageField(
                        help_text="A personal image displayed in your profile.",
                        upload_to=userena.models.upload_to_mugshot,
                        verbose_name="mugshot",
                        blank=True,
                    ),
                ),
                (
                    "privacy",
                    models.CharField(
                        default=b"registered",
                        help_text="Designates who can view your profile.",
                        max_length=15,
                        verbose_name="privacy",
                        choices=[(b"open", "Open"), (b"registered", "Registered"), (b"closed", "Closed")],
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        related_name="profile",
                        verbose_name="user",
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.deletion.PROTECT,
                    ),
                ),
            ],
            options={
                "abstract": False,
                "permissions": (("view_profile", "Can view profile"),),
            },
            bases=(models.Model,),
        ),
    ]
