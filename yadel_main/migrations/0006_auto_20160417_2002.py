# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-17 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yadel_main', '0005_auto_20160413_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='status',
            field=models.CharField(choices=[(b'new', b'new'), (b'published', b'published'), (b'pending', b'pending'), (b'rejected', b'rejected')], max_length=25),
        ),
    ]
