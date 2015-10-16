import json

from datetime import datetime
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from ..models import Event, Attendance

def delete_event(request, event_pk):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

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

    selected_dt = datetime(year=int(year_string), month=int(month_string), day=int(day_string))

    context = {
        "event": None,
        "start_date_string": selected_dt.strftime("%Y-%m-%d"),
        "start_time_string": None,
        "end_time_string": None
    }

    attendance_values = []

    try:
        event = Event.objects.get(start_dt__year=selected_dt.year, start_dt__month=selected_dt.month,
                                  start_dt__day=selected_dt.day)
        attendances = Attendance.objects.filter(event=event)

        for attendance in attendances:
            attendance_values.append(
                (attendance.member.name, "%.2f" % (attendance.attendance * 100.0, ), attendance.attendance < 0.5))

        attendance_values.sort(key=lambda x: x[0])
        context["start_date_string"] = event.start_dt.strftime("%Y-%m-%d")
        context["start_time_string"] = event.start_dt.strftime("%H:%M")
        context["end_time_string"] = event.end_dt.strftime("%H:%M")
        context["event"] = event

    except Event.DoesNotExist:
        pass

    context["attendance_values"] = attendance_values

    return render(request, 'event/edit.html', context)


def event_browser(request):
    """Return the daily process main overview page.
    """
    if not request.user.is_authenticated():
        return redirect("login")

    context = {}

    event_data = {}
    for event in Event.objects.all():
        if event.duration_minutes <= 0:
            continue
        stats = Attendance.get_stats_for_event(event)

        start_dt = event.start_dt
        end_dt = event.end_dt

        event_data[start_dt.strftime("%Y-%m-%d %H:%M")] = {
            "title": "\n%s minutes\n%.2f %% attendance\n%s players" % (
            event.duration_minutes, stats["average_attendance"] * 100.0, stats["player_count"]),
            "end_dt_string": end_dt.strftime("%Y-%m-%d %H:%M")
        }

    event_data = json.dumps(event_data)
    context["event_data"] = event_data

    return render(request, 'event/browser.html', context)