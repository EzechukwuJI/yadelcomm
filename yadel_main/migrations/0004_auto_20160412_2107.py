# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-12 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yadel_main', '0003_publication_publish_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to=b'publication/%Y-%M-%D'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='pictures',
            field=models.FileField(upload_to=b'media/'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publish_online',
            field=models.BooleanField(default=False, verbose_name=b'Do you also want online publication of the chosen media? '),
        ),
    ]
