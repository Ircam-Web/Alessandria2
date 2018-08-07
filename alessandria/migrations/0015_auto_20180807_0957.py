# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-07 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alessandria', '0014_auto_20180807_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='state',
            field=models.CharField(choices=[('available', 'Available'), ('borrowed', 'Borrowed'), ('damaged', 'Damaged'), ('lost', 'Lost'), ('withdrawed', 'Withdrawed')], default='available', max_length=32, verbose_name='state'),
        ),
    ]