# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-11 02:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialp2p', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='socialp2p.Author'),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to='socialp2p.Author'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user_can_view',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='socialp2p.Author'),
        ),
    ]
