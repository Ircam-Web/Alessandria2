# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-17 16:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alessandria', '0008_auto_20170808_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readerborrow',
            name='bookcopy',
        ),
        migrations.AddField(
            model_name='readerborrow',
            name='book',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='alessandria.Book', verbose_name='Sample'),
            preserve_default=False,
        ),
    ]
