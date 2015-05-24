# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetups', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rsvp',
            old_name='gplus_name',
            new_name='remote_username'
        ),
        migrations.RenameField(
            model_name='rsvp',
            old_name='gplus_uid',
            new_name='remote_uid'
        ),
    ]
