# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-03-04 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0008_match_can_have_penalty_shootout'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='shootout_winner',
            field=models.NullBooleanField(),
        ),
    ]
