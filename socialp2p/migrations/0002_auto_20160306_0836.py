# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-06 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialp2p', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='photo',
            field=models.ImageField(blank=True, default='socialp2p/images/profile/default-avatar.jpg', null=True, upload_to='images/profile'),
        ),
    ]