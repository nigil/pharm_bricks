# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-24 23:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180211_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='region',
        ),
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
            name='delivery_address',
            field=models.CharField(max_length=500),
        ),
    ]
