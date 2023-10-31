# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0003_auto_20180420_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressinfo',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
