# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0002_addressinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressinfo',
            name='uid',
            field=models.IntegerField(),
        ),
    ]
