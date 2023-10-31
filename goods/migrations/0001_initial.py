# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CateInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('is_del', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=100)),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('click', models.IntegerField()),
                ('sub_name', models.CharField(max_length=200)),
                ('unit', models.CharField(max_length=10)),
                ('store', models.IntegerField(default=100)),
                ('details', tinymce.models.HTMLField()),
                ('is_del', models.BooleanField(default=False)),
                ('cate', models.ForeignKey(to='goods.CateInfo')),
            ],
        ),
    ]
