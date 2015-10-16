from django.http.response import JsonResponse

from django.shortcuts import render, redirect
from ..models import Member


def report_config(request):
    """Configure report
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {}

    return render(request, 'report/report-config.html', context)
