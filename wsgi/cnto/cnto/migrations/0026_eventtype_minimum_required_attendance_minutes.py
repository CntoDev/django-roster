# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0025_set_default_absence_concluded_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtype',
            name='minimum_required_attendance_minutes',
            field=models.IntegerField(default=60),
            preserve_default=False,
        ),
    ]
