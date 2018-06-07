# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-02 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testenvData', '0003_auto_20180130_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='mobileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=30)),
                ('equip', models.CharField(max_length=50)),
                ('os', models.CharField(max_length=50)),
                ('person', models.CharField(max_length=20)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]