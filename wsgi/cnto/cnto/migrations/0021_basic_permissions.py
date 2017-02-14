# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cnto', '0020_member_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalPermission',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.permission',),
        ),
        migrations.AlterModelOptions(
            name='member',
            options={
                'permissions': (('cnto_edit_member', 'Edit members'), ('cnto_view_absentees', 'View absentees'),
                                ('cnto_view_reports', 'View reports'), ('cnto_edit_groups', 'Edit groups'),
                                ('cnto_edit_event_types', 'Edit event types'), ('cnto_view_events', 'View events'),
                                ('cnto_edit_events', 'Edit events'))
                },
        ),
    ]
