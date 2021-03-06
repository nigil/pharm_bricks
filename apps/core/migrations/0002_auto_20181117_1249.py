# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-17 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial_squashed_0002_pharmbrickssettings_footer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pharmbrickssettings',
            options={'verbose_name': 'PharmBricks settings'},
        ),
        migrations.AddField(
            model_name='pharmbrickssettings',
            name='admin_email',
            field=models.EmailField(default=b'info@pharmbricks.com', max_length=254),
        ),
        migrations.AddField(
            model_name='pharmbrickssettings',
            name='info_email',
            field=models.EmailField(default=b'info@pharmbricks.com', max_length=254),
        ),
        migrations.AddField(
            model_name='pharmbrickssettings',
            name='sender_email',
            field=models.EmailField(default=b'info@pharmbricks.com', max_length=254),
        ),
    ]
