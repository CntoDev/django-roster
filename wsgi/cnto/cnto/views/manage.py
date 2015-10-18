from django.http.response import JsonResponse, HttpResponseNotFound
from django.http import Http404
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from ..models import Member, MemberGroup, Rank
from ..forms import MemberForm


def management(request):
    """List members
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {
        "members": sorted(Member.objects.all(), key=lambda x: x.name),
        "groups": sorted(MemberGroup.objects.all(), key=lambda x: x.name)
    }

    return render(request, 'cnto/manage/main.html', context)
