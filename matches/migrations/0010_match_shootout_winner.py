# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-03-04 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0009_bet_shootout_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='shootout_winner',
            field=models.NullBooleanField(),
        ),
    ]
