from datetime import datetime, timedelta

from django.http.response import JsonResponse
from django.shortcuts import redirect

from libs.utils.attendance_scraper import get_all_event_attendances_between
from ..models import Event, Member, Rank, Attendance


def scrape(request, dt_string, start_hour, end_hour):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

    dt = datetime.strptime(dt_string, "%Y-%m-%d")

    start_dt = datetime(dt.year, dt.month, dt.day, int(start_hour), 00, 00)

    end_dt = datetime(dt.year, dt.month, dt.day, int(end_hour), 00, 00)
    if end_dt < start_dt:
        end_dt += timedelta(hours=240)

    try:
        scrape_result, scrape_stats = get_all_event_attendances_between(start_dt, end_dt)
    except ValueError:
        scrape_result = {}
        scrape_stats = {'average_attendance': 0, 'minutes': 0}

    # scrape_result = {u'Spartak [CNTO - Gnt]': 1.0, u'Chypsa [CNTO - Gnt]': 1.0, u'Guilly': 0.42857142857142855,
    # u'Hellfire [CNTO - SPC]': 1.0, u'Cody [CNTO - Gnt]': 1.0,
    # u'Ozzie [CNTO - SPC]': 0.7142857142857143, u'Skywalker': 0.6397515527950312,
    # u'Obi [CNTO - JrNCO]': 0.7142857142857143, u'Zero': 1.0,
    # u'Chris [CNTO - SPC]': 0.14285714285714285, u'Hateborder [CNTO - Gnt]': 1.0,
    # u'Dusky [CNTO - Gnt]': 0.7142857142857143}
    # scrape_stats = {'average_attendance': 0.7795031055900622, 'minutes': 56.0}
    try:
        event = Event.objects.get(start_dt__year=start_dt.year, start_dt__month=start_dt.month,
                                  start_dt__day=start_dt.day)
        event.start_dt = start_dt
        event.end_dt = end_dt
        event.duration_minutes = scrape_stats["minutes"]
        event.save()
    except Event.DoesNotExist:
        event = Event.objects.create(start_dt=start_dt, end_dt=end_dt,
                                     duration_minutes=scrape_stats["minutes"])

    previous_attendances = Attendance.objects.filter(event=event)
    previous_attendances.delete()

    for raw_username in scrape_result:
        username_parts = raw_username.split(" ")
        username = username_parts[0]
        if len(username) == 0:
            continue

        rank_str = "Rec"
        if len(username_parts) > 1:
            rank_str = username_parts[3][0:-1]
        attendance_value = scrape_result[raw_username]

        rank = Rank.get_or_create_by_name(rank_str)
        member = Member.get_or_create_by_username(username, rank=rank)

        try:
            attendance = Attendance.objects.get(event=event, member=member)
        except Attendance.DoesNotExist:
            attendance = Attendance.objects.create(event=event, member=member,
                                                   attendance=attendance_value)
        attendance.attendance = attendance_value
        attendance.save()

    return JsonResponse({"attendance": scrape_result, "stats": scrape_stats})
