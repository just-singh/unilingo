# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-29 20:17
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtubeApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportdata',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]