# -*- coding: utf-8 -*-


from django.db import migrations


def add_contribution_warning_types(apps, schema_editor):
    MemberWarningType = apps.get_model("cnto_warnings", "MemberWarningType")
    try:
        MemberWarningType.objects.get(name__iexact="Contribution Expiring")
    except MemberWarningType.DoesNotExist:
        contribution_expiring_type = MemberWarningType(name="Contribution Expiring")
        contribution_expiring_type.save()

    try:
        MemberWarningType.objects.get(name__iexact="Absence Starting")
    except MemberWarningType.DoesNotExist:
        absence_starting_type = MemberWarningType(name="Absence Starting")
        absence_starting_type.save()

    try:
        MemberWarningType.objects.get(name__iexact="Absence Ending")
    except MemberWarningType.DoesNotExist:
        absence_ending_type = MemberWarningType(name="Absence Ending")
        absence_ending_type.save()

    try:
        MemberWarningType.objects.get(name__iexact="Absence Violated")
    except MemberWarningType.DoesNotExist:
        absence_violated_type = MemberWarningType(name="Absence Violated")
        absence_violated_type.save()


def clear_warning_types(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto_warnings', '0004_memberwarning_notified'),
    ]

    operations = [
        migrations.RunPython(add_contribution_warning_types, clear_warning_types),
    ]
