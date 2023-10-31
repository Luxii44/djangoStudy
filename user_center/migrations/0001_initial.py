# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AreaInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('province_id', models.CharField(max_length=10)),
                ('city_id', models.CharField(max_length=10)),
                ('district_id', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'area',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=30)),
                ('verification', models.BooleanField(default=False)),
                ('reg_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
