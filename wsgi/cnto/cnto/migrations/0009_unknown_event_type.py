# -*- coding: utf-8 -*-


from django.db import migrations, models


def assign_unknown_event_type(apps, schema_editor):

    EventType = apps.get_model("cnto", "EventType")
    try:
        unknown_event_type = EventType.objects.get(name__iexact="unknown")
    except EventType.DoesNotExist:
        unknown_event_type = EventType(name="Unknown", default_start_hour=18, default_end_hour=21)
        unknown_event_type.save()

    Event = apps.get_model("cnto", "Event")
    for event in Event.objects.all():
        event.event_type = unknown_event_type
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0008_event_type_css'),
    ]

    operations = [
        migrations.RunPython(assign_unknown_event_type),
    ]
