# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField()),
                ('meetupcom_id', models.CharField(max_length=20, null=True, blank=True)),
                ('gplus_id', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('attendee_count', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('location', models.ForeignKey(blank=True, to='meetups.Location', null=True)),
            ],
            options={
                'ordering': ('-start_date',),
                'verbose_name': 'Meetup',
                'verbose_name_plural': 'Meetups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RSVP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True, verbose_name='Status', choices=[(b'not_coming', 'Not coming'), (b'coming', 'Coming'), (b'maybe', 'Maybe')])),
                ('gplus_name', models.CharField(max_length=100, null=True, verbose_name='Google+ Username', blank=True)),
                ('gplus_uid', models.CharField(max_length=100, null=True, verbose_name='Google+ User ID', blank=True)),
                ('source', models.CharField(max_length=20, null=True, blank=True)),
                ('meetup', models.ForeignKey(related_name='rsvps', verbose_name='Meetup', to='meetups.Meetup')),
            ],
            options={
                'verbose_name': 'RSVP',
                'verbose_name_plural': 'RSVPs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'Titel')),
                ('abstract', models.TextField(verbose_name=b'Kurzbeschreibung')),
                ('speaker_name', models.CharField(max_length=100, null=True, verbose_name=b'Vortragender', blank=True)),
                ('speaker_email', models.EmailField(max_length=75, null=True, verbose_name=b'E-Mail-Adresse', blank=True)),
                ('slides_url', models.URLField(null=True, verbose_name=b'Folien-URL', blank=True)),
                ('notes', models.TextField(null=True, verbose_name=b'Notizen', blank=True)),
                ('meetup', models.ForeignKey(related_name='sessions', verbose_name=b'Meetup', blank=True, to='meetups.Meetup', null=True)),
                ('speaker', models.ForeignKey(verbose_name=b'Vortragender', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SessionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name=b'Name')),
                ('description', models.TextField(null=True, verbose_name=b'Beschreibung', blank=True)),
            ],
            options={
                'verbose_name': 'Session type',
                'verbose_name_plural': 'Session types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='session',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Vortragsart', blank=True, to='meetups.SessionType', null=True),
            preserve_default=True,
        ),
    ]
