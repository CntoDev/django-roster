# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0016_member_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
