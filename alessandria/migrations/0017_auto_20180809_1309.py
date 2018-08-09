# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-09 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alessandria', '0016_book_manufacturer_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='classif_mark',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Classification mark'),
        ),
        migrations.AlterField(
            model_name='book',
            name='manufacturer_ref',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Manufacturer Reference'),
        ),
    ]
