import csv

import calendar
from datetime import datetime, timedelta
from django.http.response import JsonResponse
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from ..models import MemberGroup, Event, Member, Attendance, Absence, AbsenceType


def get_warnings_for_date_range(start_dt, end_dt):
    warnings = []
    events = Event.all_for_time_period(start_dt, end_dt)
    members = Member.active_members()
    for member in members:
        adequate, reason = Attendance.was_adequate_for_period(member, events, start_dt, end_dt)
        if not adequate:
            warnings.append([member, reason])

        recruit_warning, reason = member.get_recruit_warning()
        if recruit_warning:
            warnings.append([member, reason])

    return sorted(warnings, key=lambda warning: warning[0].name)


def report_main(request):
    """Browse reports
    """

    if not request.user.is_authenticated():
        return redirect("login")

    current_dt = timezone.now()
    previous_year_number = current_dt.year
    previous_month_number = current_dt.month - 1
    if previous_month_number == 0:
        previous_year_number -= 1
        previous_month_number = 12

    previous_month_start_dt = datetime(year=previous_year_number, month=previous_month_number, day=1, hour=0, minute=0)
    previous_month_end_dt = datetime(year=previous_year_number, month=previous_month_number,
                                     day=calendar.monthrange(previous_year_number, previous_month_number)[1], hour=23,
                                     minute=59)

    context = {
        "warnings": get_warnings_for_date_range(previous_month_start_dt, previous_month_end_dt)
    }

    return render(request, 'cnto/report/report-main.html', context)


def get_report_context_for_date_range(start_dt, end_dt):
    context = {}

    events = Event.all_for_time_period(start_dt, end_dt).order_by("start_dt")
    context["event_count"] = events.count()

    events_dict = {
        "start_dates": [event.start_dt.strftime("%Y-%m-%d") for event in events],
        "css_classes": [event.event_type.css_class_name for event in events]
    }
    context["events"] = events_dict

    reservist_absence_type = AbsenceType.objects.get(name__iexact="reservist")

    groups = MemberGroup.objects.all().order_by("name")
    all_members = Member.active_members_after_dt(start_dt)
    attendance_dict = {}
    for group in groups:
        attendance_dict[group.name] = {}
        members = all_members.filter(member_group=group).order_by("name")
        for member in members:
            period_attendance_adequate, reason = Attendance.was_adequate_for_period(member, events, start_dt, end_dt)
            attendance_dict[group.name][member.name] = {
                "attendance_adequate": period_attendance_adequate,
                "attendances": []
            }
            for event in events:
                try:
                    if member.join_dt > event.start_dt:
                        absence_type = "-"
                    else:
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