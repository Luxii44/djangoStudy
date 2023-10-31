# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0004_auto_20180420_2217'),
        ('goods', '0002_auto_20180421_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=36, serialize=False)),
                ('count', models.IntegerField(default=1)),
                ('goods', models.ForeignKey(to='goods.GoodsInfo')),
                ('user', models.ForeignKey(to='user_center.UserInfo')),
            ],
        ),
    ]
