# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-22 14:56
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

import matches.models


class Migration(migrations.Migration):
    dependencies = [
        ('matches', '0005_bet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='away_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='home_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bet',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matches.Match',
                                    validators=[matches.models.validate_match_datetime]),
        ),
    ]
