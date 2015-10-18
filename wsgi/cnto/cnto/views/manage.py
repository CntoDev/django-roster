from django.http.response import JsonResponse, HttpResponseNotFound
from django.http import Http404
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from ..models import Member, MemberGroup, Rank, EventType
from ..forms import MemberForm


def management(request):
    """List members
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {
        "members": sorted(Member.objects.all().filter(discharged=False), key=lambda x: x.name.lower()),
        "discharges": sorted(Member.objects.all().filter(discharged=True), key=lambda x: x.name.lower()),
        "groups": sorted(MemberGroup.objects.all(), key=lambda x: x.name.lower()),
        "event_types": sorted(EventType.objects.all(), key=lambda x: x.name.lower())
    }

    return render(request, 'cnto/manage/main.html', context)
