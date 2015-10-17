import csv

from datetime import datetime
from django.http import HttpResponse
from ..models import MemberGroup, Event, Member, Attendance

def download_report_for_month(request, dt_string, group_pk=None):
    group = MemberGroup.objects.get(pk=group_pk)
    dt = datetime.strptime(dt_string, "%Y-%m-%d")

    events = Event.objects.filter(start_dt__year=dt.year, start_dt__month=dt.month).order_by("start_dt")

    members = Member.objects.filter(member_group=group).order_by("name")

    filename = "%s-%s.csv" % (dt_string, group.name.lower())

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
            event_attendance = 0
            try:
                attendance = Attendance.objects.get(member=member, event=event)
                event_attendance = attendance.attendance
            except Attendance.DoesNotExist:
                pass

            member_columns.append("%.2f" % (event_attendance, ))

        writer.writerow(member_columns)

    return response