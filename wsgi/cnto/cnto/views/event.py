import json

from datetime import datetime
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from ..models import Event, Attendance, MemberGroup, EventType
from django.http import Http404
from django.template.context_processors import csrf
from cnto.templatetags.cnto_tags import has_permission

from ..forms import EventTypeForm


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

    selected_dt = datetime(year=int(year_string), month=int(month_string), day=int(day_string))

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
        attendances = Attendance.objects.filter(event=event)

        for attendance in attendances:
            attendance_values.append(
                (attendance.member.name, "%.2f" % (attendance.attendance * 100.0, ),
                 not attendance.was_adequate()))

        attendance_values.sort(key=lambda x: x[0])
        context["start_date_string"] = event.start_dt.strftime("%Y-%m-%d")
        context["start_time_string"] = event.start_dt.strftime("%H:%M")
        context["end_time_string"] = event.end_dt.strftime("%H:%M")
        context["event"] = event

    except Event.DoesNotExist:
        pass

    context["attendance_values"] = attendance_values

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
    for event in Event.objects.all():
        stats = Attendance.get_stats_for_event(event)

        start_dt = event.start_dt
        end_dt = event.end_dt

        event_data[start_dt.strftime("%Y-%m-%d %H:%M")] = {
            "title": "\n%s minutes\n%.2f %% attendance\n%s players" % (
                event.duration_minutes, stats["average_attendance"] * 100.0, stats["player_count"]),
            "end_dt_string": end_dt.strftime("%Y-%m-%d %H:%M"),
            "css_class_name": event.event_type.css_class_name,
        }

    event_data = json.dumps(event_data)
    context["event_data"] = event_data
    context["groups"] = MemberGroup.objects.all()

    return render(request, 'cnto/event/browser.html', context)
