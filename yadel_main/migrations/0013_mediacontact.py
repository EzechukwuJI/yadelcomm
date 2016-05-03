# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-30 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yadel_main', '0012_auto_20160428_2322'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.CharField(max_length=125)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('contact_email', models.CharField(max_length=225)),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yadel_main.MediaNames')),
            ],
        ),
    ]
