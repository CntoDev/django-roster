# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0012_verbose_join_date_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='discharged',
            field=models.BooleanField(default=False),
        ),
    ]
