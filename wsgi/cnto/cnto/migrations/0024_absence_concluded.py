# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0023_edit_member_permission_changed'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='concluded',
            field=models.BooleanField(default=False),
        ),
    ]
