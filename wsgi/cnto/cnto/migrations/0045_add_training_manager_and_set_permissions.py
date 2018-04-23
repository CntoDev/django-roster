# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType

from django.db import migrations


def add_permission_to_group(apps, schema_editor, permission_name, role_name, with_create_permissions=True):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    Member = apps.get_model("cnto", "Member")
    try:

        content_type = ContentType.objects.get_for_model(Member)
        perm, created = Permission.objects.get_or_create(
            codename=permission_name,
            content_type=content_type)
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
        training_manager_group = Group.objects.get(name__iexact="TrainingManager")
    except Group.DoesNotExist:
        training_manager_group = Group(name="TrainingManager")
        training_manager_group.save()
    training_manager_group.permissions.clear()

    add_permission_to_group(apps, schema_editor, "cnto_view_reports", "TrainingManager")


def clear_groups(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0044_auto_20170420_2227'),
    ]

    operations = [
        migrations.RunPython(add_groups_and_set_permissions, clear_groups),
    ]
