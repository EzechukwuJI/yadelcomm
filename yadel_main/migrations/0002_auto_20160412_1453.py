# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-12 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yadel_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='title',
            field=models.CharField(max_length=15),
        ),
    ]