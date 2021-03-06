# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-11 11:28
from __future__ import unicode_literals

from django.db import migrations, models
import mols.models


class Migration(migrations.Migration):

    dependencies = [
        ('mols', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='molecule',
            name='catalogue_number',
            field=models.CharField(max_length=20, unique=True, verbose_name='Catalogue number'),
        ),
        migrations.AlterField(
            model_name='molecule',
            name='image',
            field=models.ImageField(upload_to=mols.models.mol_image_path),
        ),
    ]
