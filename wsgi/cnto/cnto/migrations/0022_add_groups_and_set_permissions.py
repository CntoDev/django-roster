# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_permission_to_group(apps, schema_editor, permission_name, role_name, with_create_permissions=True):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    try:
        perm, created = Permission.objects.get_or_create(
            codename=permission_name, content_type__name='global_permission')
    except Permission.DoesNotExist:
        if with_create_permissions:
            # Manually run create_permissions
            from django.contrib.auth.management import create_permissions
            assert not getattr(apps, 'models_module', None)
            apps.models_module = True
            create_permissions(apps, verbosity=0)
            apps.models_module = None
            return add_permission_to_group(
                apps, schema_editor, permission_name, role_name, with_create_permissions=False)
        else:
            raise

    group = Group.objects.get(name__iexact=role_name)
    group.permissions.add(perm)
    return perm


def add_groups_and_set_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    try:
        officer_group = Group.objects.get(name__iexact="Officer")
    except Group.DoesNotExist:
        officer_group = Group(name="Officer")
        officer_group.save()
    officer_group.permissions.clear()

    try:
        interviewer_group = Group.objects.get(name__iexact="Interviewer")
    except Group.DoesNotExist:
        interviewer_group = Group(name="Interviewer")
        interviewer_group.save()
    interviewer_group.permissions.clear()

    add_permission_to_group(apps, schema_editor, "cnto_edit_members", "Officer")
    # add_permission_to_group(apps, schema_editor, "cnto_edit_members", "Interviewer")

    add_permission_to_group(apps, schema_editor, "cnto_view_absentees", "Officer")
    # add_permission_to_group(apps, schema_editor, "cnto_view_absentees", "Interviewer")

    add_permission_to_group(apps, schema_editor, "cnto_view_reports", "Officer")
    # add_permission_to_group(apps, schema_editor, "cnto_view_reports", interviewer_group)

    # officer_group.permissions.add(Permission.objects.get(name='cnto_edit_groups'))
    # interviewer_group.permissions.add(Permission.objects.get(name='cnto_edit_groups'))

    # officer_group.permissions.add(Permission.objects.get(name='cnto_edit_event_types'))
    # interviewer_group.permissions.add(Permission.objects.get(name='cnto_edit_event_types'))

    add_permission_to_group(apps, schema_editor, "cnto_view_events", "Officer")
    # add_permission_to_group(apps, schema_editor, "cnto_view_events", interviewer_group)

    # officer_group.permissions.add(Permission.objects.get(name='cnto_edit_events'))
    # interviewer_group.permissions.add(Permission.objects.get(name='cnto_edit_events'))


def clear_groups(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0021_basic_permissions'),
    ]

    operations = [
        migrations.RunPython(add_groups_and_set_permissions, clear_groups),
    ]
