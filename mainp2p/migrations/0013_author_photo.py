# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-06 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainp2p', '0012_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='photo',
            field=models.ImageField(null=True, upload_to='images/profile'),
        ),
    ]