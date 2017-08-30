# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0002_event_dts'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duration_minutes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
