# -*- coding: utf-8 -*-


from django.db import migrations


def add_basic_warning_types(apps, schema_editor):
    MemberWarningType = apps.get_model("cnto_warnings", "MemberWarningType")
    try:
        MemberWarningType.objects.get(name__iexact="Low Attendance")
    except MemberWarningType.DoesNotExist:
        low_attendance_type = MemberWarningType(name="Low Attendance")
        low_attendance_type.save()

    try:
        MemberWarningType.objects.get(name__iexact="Mod Assessment Due")
    except MemberWarningType.DoesNotExist:
        mod_assessment_type = MemberWarningType(name="Mod Assessment Due")
        mod_assessment_type.save()

    try:
        MemberWarningType.objects.get(name__iexact="Grunt Qualification Due")
    except MemberWarningType.DoesNotExist:
        grunt_qualification_type = MemberWarningType(name="Grunt Qualification Due")
        grunt_qualification_type.save()


def clear_warning_types(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto_warnings', '0002_general_warning'),
    ]

    operations = [
        migrations.RunPython(add_basic_warning_types, clear_warning_types),
    ]
