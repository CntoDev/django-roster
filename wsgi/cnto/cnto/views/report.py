import csv

from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from ..models import MemberGroup, Event, Member, Attendance


def report_browser(request):
    """Browse reports
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {}

    return render(request, 'cnto/report/report-browser.html', context)


def get_report_context_for_date_range(start_dt, end_dt):
    context = {}

    events = Event.objects.filter(start_dt__gte=start_dt, start_dt__lte=end_dt)
    context["event_count"] = events.count()
    context["start_dt"] = start_dt
    context["end_dt"] = end_dt

    return context


def get_report_body(request):
    """Get reports
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = get_report_context_for_date_range(datetime(2015, 9, 1, 0, 0), datetime(2015, 9, 30, 23, 59))

    return render(request, 'cnto/report/report-body.html', context)


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