# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0041_member_bqf_assessed'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='bi_name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
