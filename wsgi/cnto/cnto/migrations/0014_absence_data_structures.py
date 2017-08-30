    # -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0013_member_discharged'),
    ]

    operations = [
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_dt', models.DateTimeField()),
                ('end_dt', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='AbsenceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='absence',
            name='absence_type',
            field=models.ForeignKey(to='cnto.AbsenceType'),
        ),
        migrations.AddField(
            model_name='absence',
            name='member',
            field=models.ForeignKey(to='cnto.Member'),
        ),
    ]
