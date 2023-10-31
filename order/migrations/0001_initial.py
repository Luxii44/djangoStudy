# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20180421_1917'),
        ('user_center', '0004_auto_20180420_2217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=20, serialize=False)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('state', models.IntegerField(default=0)),
                ('address', models.ForeignKey(to='user_center.AddressInfo')),
                ('user', models.ForeignKey(to='user_center.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('count', models.IntegerField()),
                ('price', models.DecimalField(default=0, max_digits=5, decimal_places=2)),
                ('goods', models.ForeignKey(to='goods.GoodsInfo')),
                ('order', models.ForeignKey(to='order.Order')),
            ],
        ),
    ]
