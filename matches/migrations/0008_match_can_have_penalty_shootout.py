# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-03-04 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0007_auto_20170822_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='can_have_penalty_shootout',
            field=models.BooleanField(default=False),
        ),
    ]
