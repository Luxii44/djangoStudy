# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cateinfo',
            table='cates',
        ),
        migrations.AlterModelTable(
            name='goodsinfo',
            table='goods',
        ),
    ]
