# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0007_event_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtype',
            name='css_class_name',
            field=models.TextField(blank=True),
        ),
    ]
