# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-21 21:49
from __future__ import unicode_literals

import core.storage
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import screening_libraries.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0007_merge'),
        ('wagtailcore', '0040_page_draft_title'),
        ('screening_libraries', '0002_auto_20180820_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreeningLibrariyPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(max_length=32, verbose_name='Quantity')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('price',),
            },
        ),
        migrations.CreateModel(
            name='ScreeningLibrary',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('catalogue_number', models.CharField(max_length=20, unique=True)),
                ('preview_description', models.TextField(blank=True, null=True)),
                ('preview_image', models.ImageField(blank=True, null=True, storage=core.storage.OverwriteStorage(), upload_to=screening_libraries.models.screening_libraries_image_path)),
                ('detail_image', models.ImageField(blank=True, null=True, storage=core.storage.OverwriteStorage(), upload_to=screening_libraries.models.screening_libraries_detail_image_path)),
                ('molecules_number', models.IntegerField(default=1)),
                ('in_stock', models.BooleanField(default=True)),
                ('sdf_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document')),
                ('xls_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.AddField(
            model_name='screeninglibrariyprices',
            name='product',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='screening_libraries.ScreeningLibrary'),
        ),
    ]
