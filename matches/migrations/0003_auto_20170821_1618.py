# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0002_bet'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='away_score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bet',
            name='home_score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
