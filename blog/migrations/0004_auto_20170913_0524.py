# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-13 05:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170912_0730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crawler',
            name='Data',
        ),
        migrations.RemoveField(
            model_name='crawler',
            name='Pic',
        ),
    ]
