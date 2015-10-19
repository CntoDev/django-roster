import csv

import calendar
from datetime import datetime
from django.http.response import JsonResponse
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from ..models import MemberGroup, Event, Member, Attendance, Absence, AbsenceType


def report_browser(request):
    """Browse reports
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {}

    return render(request, 'cnto/report/report-browser.html', context)


def get_report_context_for_date_range(start_dt, end_dt):
    context = {}

    events = Event.objects.filter(start_dt__gte=start_dt, start_dt__lte=end_dt).order_by("start_dt")
    context["event_count"] = events.count()

    events_dict = {
        "start_dates": [event.start_dt.strftime("%Y-%m-%d") for event in events],
        "css_classes": [event.event_type.css_class_name for event in events]
    }
    context["events"] = events_dict

    reservist_absence_type = AbsenceType.objects.get(name__iexact="reservist")

    groups = MemberGroup.objects.all().order_by("name")
    attendance_dict = {}
    for group in groups:
        attendance_dict[group.name] = {}
        members = Member.objects.filter(member_group=group).order_by("name")
        for member in members:
            attendance_dict[group.name][member.name] = {
                "attendance_adequate": Attendance.was_adequate_for_period(member, events, start_dt, end_dt),
                "attendances": []
            }
            for event in events:
                try:
                    absence = Absence.objects.get(member=member, start_dt__lte=event.start_dt,
                                                  end_dt__gte=event.start_dt)
                    if absence.absence_type == reservist_absence_type:
                        absence_type = "R"
                    else:
                        absence_type = "LOA"
                except Absence.DoesNotExist:
                    absence_type = None

                if absence_type is not None:
                    presence_marker = absence_type
                else:
                    try:
                        attendance = Attendance.objects.get(member=member, event=event)
                        was_adequate = attendance.was_adequate()
                        if was_adequate:
                            presence_marker = "X"
                        else:
                            presence_marker = "?"

                    except Attendance.DoesNotExist:
                        presence_marker = " "




                attendance_dict[group.name][member.name]["attendances"].append(presence_marker)

    context["attendances"] = attendance_dict

    context["start_dt"] = start_dt.strftime("%Y-%m-%d")
    context["end_dt"] = end_dt.strftime("%Y-%m-%d")

    return context


def get_report_body_for_month(request, month_string):
    """Get reports
    """
    if not request.user.is_authenticated():
        return redirect("login")

    month_dt = datetime.strptime(month_string, "%Y-%m")

    context = get_report_context_for_date_range(datetime(month_dt.year, month_dt.month, 1, 0, 0),
                                                datetime(month_dt.year, month_dt.month,
                                                         calendar.monthrange(month_dt.year, month_dt.month)[1], 23, 59))

    return JsonResponse(context)


def download_report_for_month(request, dt_string, group_pk=None):
    if not request.user.is_authenticated():
        return HttpResponse("Unauthorised", status=403)

    group = MemberGroup.objects.get(pk=group_pk)
    dt = datetime.strptime(dt_string, "%Y-%m-%d")

    events = Event.objects.filter(start_dt__year=dt.year, start_dt__month=dt.month).order_by("start_dt")

    members = Member.objects.filter(member_group=group).order_by("name")

    filename = "%s-%s.csv" % (dt.strftime("%Y-%m"), group.name.lower())

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename, )
    writer = csv.writer(response)

    header_columns = ["Member"]
    for event in events:
        header_columns.append(event.start_dt.strftime("%Y-%m-%d"))
    writer.writerow(header_columns)

    for member in members:
        member_columns = [member.name]

        for event in events:
            was_adequate = False
            try:
                attendance = Attendance.objects.get(member=member, event=event)
                was_adequate = attendance.was_adequate()
            except Attendance.DoesNotExist:
                pass

            if was_adequate:
                member_columns.append("X")
            else:
                member_columns.append(" ")

        writer.writerow(member_columns)

    writer.writerow([])
    writer.writerow(["X = attended"])

    return response