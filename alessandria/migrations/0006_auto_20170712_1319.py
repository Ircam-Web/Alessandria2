# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-12 13:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alessandria', '0005_auto_20170712_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='classif_mark',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Classification mark'),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alessandria.Language', verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateField(blank=True, null=True, verbose_name='Publishing date'),
        ),
    ]