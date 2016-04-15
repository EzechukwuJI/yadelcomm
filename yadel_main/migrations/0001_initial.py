# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-12 13:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(max_length=150)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MediaNames',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_name', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=175)),
                ('title_slug', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[(b'Published', b'published'), (b'Pending', b'pending'), (b'Rejected', b'rejected')], max_length=25)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=3000)),
                ('pictures', models.FileField(upload_to=b'/media/')),
                ('deleted', models.BooleanField(default=False)),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yadel_main.MediaNames')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('press_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yadel_main.MediaCategory')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[(b'Mr', b'Mr'), (b'Mrs', b'Mrs'), (b'Dr', b'Dr')], max_length=15)),
                ('phone_no', models.CharField(max_length=15)),
                ('organization', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('registration_code', models.CharField(max_length=25)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
