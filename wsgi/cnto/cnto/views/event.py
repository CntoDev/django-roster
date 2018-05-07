import json
import traceback

from django.db import models
from django.utils import timezone
from django.utils.timezone import datetime
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.http import Http404
from django.template.context_processors import csrf
from datetime import timedelta
from cnto_warnings.models import MemberWarning
from ..models import Event, Attendance, MemberGroup, EventType
from cnto.templatetags.cnto_tags import has_permission
from ..forms import EventTypeForm
from utils.date_utils import calculate_dt_from_strings


def delete_event_type(request, event_type_pk):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_edit_event_types"):
        return redirect("manage")

    try:
        event_type = EventType.objects.get(pk=event_type_pk)
        event_type.delete()
        return JsonResponse({"success": True})
    except Event.DoesNotExist:
        return JsonResponse({"success": False})


def handle_event_type_change_view(request, edit_mode, event_type=None):
    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_edit_event_types"):
        return redirect("manage")

    if request.POST:
        form = EventTypeForm(request.POST, instance=event_type)
        if request.POST.get("cancel"):
            return redirect('manage')
        elif form.is_valid():
            form.save()
            return redirect('manage')
    else:
        form = EventTypeForm(instance=event_type)

    context = {}
    context.update(csrf(request))

    context['form'] = form
    context["edit_mode"] = edit_mode

    return render_to_response('cnto/event/edit-type.html', context)


def create_event_type(request):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_edit_event_types"):
        return redirect("manage")

    return handle_event_type_change_view(request, edit_mode=False)


def edit_event_type(request, pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_edit_event_types"):
        return redirect("manage")

    try:
        event_type = EventType.objects.get(pk=pk)
    except MemberGroup.DoesNotExist:
        raise Http404()

    return handle_event_type_change_view(request, edit_mode=True, event_type=event_type)


def delete_event(request, event_pk):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_edit_events"):
        return redirect("manage")

    try:
        event = Event.objects.get(pk=event_pk)
        event.delete()
        return JsonResponse({"success": True})
    except Event.DoesNotExist:
        return JsonResponse({"success": False})


def view_event(request, year_string, month_string, day_string):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_view_events"):
        return redirect("manage")

    selected_dt = timezone.make_aware(datetime(year=int(year_string), month=int(month_string), day=int(day_string)),
                                      timezone.get_default_timezone())

    context = {
        "event": None,
        "event_types": EventType.objects.all().order_by("name"),
        "start_date_string": selected_dt.strftime("%Y-%m-%d"),
        "start_time_string": None,
        "end_time_string": None,
    }

    attendance_values = []

    try:
        event = Event.objects.get(start_dt__year=selected_dt.year, start_dt__month=selected_dt.month,
                                  start_dt__day=selected_dt.day)
        attendances = Attendance.objects.filter(event=event, member__deleted=False)

        for attendance in attendances:
            attendance_values.append(
                (attendance.member.name, "%.2f" % (attendance.get_attendance_ratio() * 100.0,),
                 not attendance.was_adequate()))

        attendance_values.sort(key=lambda x: x[0])

        context["start_date_string"] = event.start_dt.astimezone(timezone.get_default_timezone()).strftime("%Y-%m-%d")
        context["start_time_string"] = event.start_dt.astimezone(timezone.get_default_timezone()).strftime("%H:%M")
        context["end_time_string"] = event.end_dt.astimezone(timezone.get_default_timezone()).strftime("%H:%M")
        context["event"] = event

    except Event.DoesNotExist:
        pass

    context["attendance_values"] = attendance_values
    context["warning_count"] = MemberWarning.objects.filter(acknowledged=False).count()

    return render(request, 'cnto/event/edit.html', context)


def event_browser(request):
    """Return the daily process main overview page.
    """
    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_view_events"):
        return redirect("manage")

    context = {}

    event_data = {}
    for event in Event.objects.all().select_related(
        'event_type',
    ).prefetch_related(
        models.Prefetch('attendees', queryset=Attendance.objects.all()),
    ):
        stats = event.get_stats()

        start_dt = event.start_dt
        end_dt = event.end_dt

        event_data[start_dt.astimezone(timezone.get_default_timezone()).strftime("%Y-%m-%d %H:%M")] = {
            "title": "\n%s minutes\n%.2f %% attendance\n%s players" % (
                event.duration_minutes, stats["average_attendance"] * 100.0, stats["player_count"]),
            "end_dt_string": end_dt.astimezone(timezone.get_default_timezone()).strftime("%Y-%m-%d %H:%M"),
            "css_class_name": event.event_type.css_class_name,
        }

    event_data = json.dumps(event_data)
    context["event_data"] = event_data
    context["groups"] = MemberGroup.objects.all()
    context["warning_count"] = MemberWarning.objects.filter(acknowledged=False).count()

    return render(request, 'cnto/event/browser.html', context)


def save_event(request, event_type_name, dt_string, start_time_string, end_time_string):
    """Return the daily process main overview page.
    """

    try:
        if not request.user.is_authenticated():
            return redirect("login")
        elif not has_permission(request.user, "cnto_edit_events"):
            return redirect("manage")

        event_type = EventType.objects.get(name__iexact=event_type_name)

        start_dt = calculate_dt_from_strings(dt_string, start_time_string)
        end_dt = calculate_dt_from_strings(dt_string, end_time_string)

        if end_dt < start_dt:
            end_dt += timedelta(hours=24)

        event = Event.objects.get(start_dt__year=start_dt.year, start_dt__month=start_dt.month,
                                  start_dt__day=start_dt.day)

        event.start_dt = start_dt
        event.end_dt = end_dt

        event.event_type = event_type
        event.duration_minutes = (end_dt - start_dt).total_seconds() / 60
        event.save()
    except Exception:
        return JsonResponse({"success": False, "error": traceback.format_exc()})

    return JsonResponse({"success": True, "error": None})
