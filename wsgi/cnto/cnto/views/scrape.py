from datetime import datetime

from django.shortcuts import render, redirect
from utils.attendance_scraper import get_all_event_attendances_between


def scrape_selection(request):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {}
    return render(request, 'scrape-selection.html', context)


def scrape(request):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

    start_dt = datetime(2015, 10, 10, 18, 00, 00)
    end_dt = datetime(2015, 10, 12, 20, 00, 00)

    scrape_result = get_all_event_attendances_between(start_dt, end_dt)

    context = {"result": scrape_result}
    return render(request, 'scrape.html', context)
