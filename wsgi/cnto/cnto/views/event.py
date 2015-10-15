from datetime import datetime
from django.core.urlresolvers import reverse

from django.shortcuts import render, redirect
from libs.utils.attendance_scraper import get_all_event_attendances_between


def view_date(request, year_string, month_string, day_string):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

    selected_dt = datetime(year=int(year_string), month=int(month_string), day=int(day_string))

    context = {}
    context["date_string"] = selected_dt.strftime("%Y-%m-%d")
    context["return_url"] = reverse("scrape-selection")

    return render(request, 'view-date.html', context)
