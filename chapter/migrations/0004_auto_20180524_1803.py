# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-05-24 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chapter', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(verbose_name='\u8bc4\u8bba\u5185\u5bb9'),
        ),
    ]
