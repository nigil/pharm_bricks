# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-25 00:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180624_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.City'),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.Country'),
        ),
    ]
