# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-04 06:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainp2p', '0017_auto_20160304_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/post'),
        ),
    ]