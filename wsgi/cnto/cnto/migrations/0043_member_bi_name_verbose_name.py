# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0042_member_bi_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='bi_name',
            field=models.TextField(verbose_name=b'BI nickname'),
        ),
    ]
