# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto_warnings', '0003_add_basic_warning_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberwarning',
            name='notified',
            field=models.BooleanField(default=False),
        ),
    ]
