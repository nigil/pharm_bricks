# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-26 01:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screening_libraries', '0006_auto_20180826_0051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='screeninglibrary',
            old_name='preview_image',
            new_name='image',
        ),
    ]
