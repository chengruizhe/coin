# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 03:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0004_auto_20171008_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='studygroup',
            name='processed_pic',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='processed'),
            preserve_default=False,
        ),
    ]
