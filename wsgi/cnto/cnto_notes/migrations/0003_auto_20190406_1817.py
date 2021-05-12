# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cnto_notes', '0002_auto_20170420_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='member',
            field=models.ForeignKey(to='cnto.Member', related_name='notes'),
        ),
    ]
