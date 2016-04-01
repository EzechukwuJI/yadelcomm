# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=175)),
                ('title_slug', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=25, choices=[(b'Published', b'published'), (b'Pending', b'pending'), (b'Rejected', b'rejected')])),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(max_length=50, choices=[(b'news', b'news'), (b'socials', b'socials'), (b'promo', b'promo'), (b'alert', b'alert'), (b'others', b'others')])),
                ('content', models.CharField(max_length=1500)),
                ('pictures', models.FileField(upload_to=b'/media/')),
                ('deleted', models.BooleanField(default=False)),
                ('posted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_no', models.CharField(max_length=15)),
                ('organization', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
