# -*- coding: utf-8 -*-


from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0027_member_names_not_unique'),
        ('cnto_warnings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberWarning',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.TextField()),
                ('acknowledged', models.BooleanField(default=False)),
                ('member', models.ForeignKey(to='cnto.Member')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MemberWarningType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='lowattendancewarning',
            name='member',
        ),
        migrations.DeleteModel(
            name='LowAttendanceWarning',
        ),
        migrations.AddField(
            model_name='memberwarning',
            name='warning_type',
            field=models.ForeignKey(to='cnto_warnings.MemberWarningType'),
        ),
    ]
