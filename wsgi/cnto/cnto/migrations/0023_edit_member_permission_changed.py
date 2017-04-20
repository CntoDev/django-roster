# -*- coding: utf-8 -*-


from django.db import migrations, models


def fix_permission_name(apps, schema_editor):
    Permission = apps.get_model("auth", "Permission")

    ContentType = apps.get_model("contenttypes", "ContentType")
    Member = apps.get_model("cnto", "Member")
    content_type = ContentType.objects.get_for_model(Member)

    try:
        perm = Permission.objects.get(
            codename="cnto_edit_member", content_type=content_type)

        perm.codename = "cnto_edit_members"
        perm.save()
    except Permission.DoesNotExist:
        perm = Permission.objects.get(
            codename="cnto_edit_members", content_type=content_type)
        assert perm is not None


def break_permission_name(apps, schema_editor):
    Permission = apps.get_model("auth", "Permission")

    ContentType = apps.get_model("contenttypes", "ContentType")
    Member = apps.get_model("cnto", "Member")
    content_type = ContentType.objects.get_for_model(Member)
    try:
        perm = Permission.objects.get(
            codename="cnto_edit_members", content_type=content_type)
        perm.codename = "cnto_edit_member"
        perm.save()
    except Permission.DoesNotExist:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0022_add_groups_and_set_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'permissions': (('cnto_edit_members', 'Edit members'), ('cnto_view_absentees', 'View absentees'), ('cnto_view_reports', 'View reports'), ('cnto_edit_groups', 'Edit groups'), ('cnto_edit_event_types', 'Edit event types'), ('cnto_view_events', 'View events'), ('cnto_edit_events', 'Edit events'))},
        ),

        migrations.RunPython(fix_permission_name, break_permission_name),
    ]
