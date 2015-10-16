from django.http.response import JsonResponse

from django.shortcuts import render, redirect
from ..models import Member


def delete_member(request, member_pk):
    """Delete Member
    """

    if not request.user.is_authenticated():
        return redirect("login")

    try:
        member = Member.objects.get(pk=member_pk)
        member.delete()
    except Member.DoesNotExist:
        return JsonResponse({"success": False})
    return JsonResponse({"success": True})


def edit_member(request, member_pk):
    """View Member
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {}

    return render(request, 'member/report-config.html', context)


def list_members(request):
    """List members
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {
        "members": sorted(Member.objects.all(), key=lambda x: x.name)
    }

    return render(request, 'member/list.html', context)
