# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-08 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mols', '0009_auto_20180708_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='moleculereference',
            name='sort_order',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]
