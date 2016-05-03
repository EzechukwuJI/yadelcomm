# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-20 22:22
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yadel_main', '0008_auto_20160417_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 20, 22, 22, 9, 633956, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='published_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Edited_and_published_by', to=settings.AUTH_USER_MODEL),
        ),
    ]