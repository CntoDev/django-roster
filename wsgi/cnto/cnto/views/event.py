from datetime import datetime
from django.core.urlresolvers import reverse

from django.shortcuts import render, redirect
from libs.utils.attendance_scraper import get_all_event_attendances_between
from ..models import Attendance, Event


def view_event(request, year_string, month_string, day_string):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

    selected_dt = datetime(year=int(year_string), month=int(month_string), day=int(day_string))

    context = {
        "date_string": selected_dt.strftime("%Y-%m-%d"),
        "return_url": reverse("scrape-selection")
    }

    attendance_values = []

    try:
        event = Event.objects.get(start_dt__year=selected_dt.year, start_dt__month=selected_dt.month,
                                  start_dt__day=selected_dt.day)
        attendances = Attendance.objects.filter(event=event)

        for attendance in attendances:
            attendance_values.append((attendance.member.name, "%.2f" % (attendance.attendance * 100.0, )))

        attendance_values.sort(key=lambda x: x[0])

    except Event.DoesNotExist:
        pass

    context["attendance_values"] = attendance_values

    return render(request, 'view-event.html', context)
