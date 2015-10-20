# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0020_member_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Note date')),
                ('active', models.BooleanField(default=True)),
                ('member', models.ForeignKey(to='cnto.Member')),
            ],
        ),
    ]
