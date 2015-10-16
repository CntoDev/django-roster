# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0004_unique_member_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membergroup',
            name='name',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='rank',
            name='name',
            field=models.TextField(unique=True),
        ),
    ]
