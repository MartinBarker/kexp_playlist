# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-26 00:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='plays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playid', models.CharField(max_length=250)),
                ('playtypeid', models.IntegerField(null=True)),
                ('playtypename', models.CharField(max_length=250)),
                ('airdate', models.DateTimeField()),
                ('artistname', models.CharField(max_length=250, null=True)),
                ('releasename', models.CharField(max_length=250, null=True)),
                ('releaseImage', models.CharField(max_length=250, null=True)),
                ('releaseYear', models.DateField(null=True)),
                ('trackName', models.CharField(max_length=250, null=True)),
                ('comment', models.CharField(max_length=250, null=True)),
            ],
        ),
    ]
