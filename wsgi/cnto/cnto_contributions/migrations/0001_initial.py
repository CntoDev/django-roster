# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0030_remove_dts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('member', models.ForeignKey(to='cnto.Member')),
            ],
            options={
                'permissions': (('cnto_edit_contributions', 'Edit contributions'),),
            },
        ),
        migrations.CreateModel(
            name='ContributionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='contribution',
            name='type',
            field=models.ForeignKey(to='cnto_contributions.ContributionType'),
        ),
    ]
