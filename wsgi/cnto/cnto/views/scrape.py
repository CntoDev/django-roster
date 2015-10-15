from datetime import datetime
from django.http.response import JsonResponse

from django.shortcuts import render, redirect
from libs.utils.attendance_scraper import get_all_event_attendances_between


def scrape_selection(request):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {}
    return render(request, 'scrape-selection.html', context)


def scrape(request, dt_string, start_hour, end_hour):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

    dt = datetime.strptime(dt_string, "%Y-%m-%d")

    start_dt = datetime(dt.year, dt.month, dt.day, int(start_hour), 00, 00)
    end_dt = datetime(dt.year, dt.month, dt.day, int(end_hour), 00, 00)

    scrape_result = get_all_event_attendances_between(start_dt, end_dt)

    return JsonResponse({"attendance": scrape_result[0], "stats": scrape_result[1]})
