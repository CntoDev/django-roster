# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0026_eventtype_minimum_required_attendance_minutes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.TextField(),
        ),
    ]
