# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 00:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0002_auto_20171007_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studygroup',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='studygroup',
            name='picture',
            field=models.ImageField(upload_to='studygroups'),
        ),
        migrations.AlterField(
            model_name='studygroup',
            name='slack_id',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
