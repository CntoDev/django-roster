# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0032_auto_20151215_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtype',
            name='minimum_required_attendance_ratio',
            field=models.FloatField(),
        ),
    ]
