# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-06 08:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180626_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.City'),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.Country'),
        ),
        migrations.AlterField(
            model_name='user',
            name='postcode',
            field=models.CharField(max_length=20),
        ),
    ]
