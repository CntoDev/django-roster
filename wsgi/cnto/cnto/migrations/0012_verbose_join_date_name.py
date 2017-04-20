# -*- coding: utf-8 -*-


from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0011_added_join_dt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='join_dt',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Join date'),
        ),
    ]
