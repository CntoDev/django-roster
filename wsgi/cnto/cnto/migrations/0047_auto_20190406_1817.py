# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0046_new_rank_cpl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='member',
            field=models.ForeignKey(to='cnto.Member', related_name='absences'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='event',
            field=models.ForeignKey(to='cnto.Event', related_name='attendees'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='member',
            field=models.ForeignKey(to='cnto.Member', related_name='attendances'),
        ),
    ]
