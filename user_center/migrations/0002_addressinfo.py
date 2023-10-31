# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('uid', models.IntegerField(max_length=10)),
                ('realname', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=100)),
                ('province_id', models.CharField(max_length=10)),
                ('city_id', models.CharField(max_length=10)),
                ('district_id', models.CharField(max_length=10)),
                ('is_default', models.BooleanField()),
            ],
            options={
                'db_table': 'user_address',
            },
        ),
    ]
