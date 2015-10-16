from django.http.response import JsonResponse

from django.shortcuts import render, redirect


def delete_member(request, member_pk):
    """Delete Member
    """

    if not request.user.is_authenticated():
        return redirect("login")

    # try:
    #     # event = Event.objects.get(pk=event_pk)
    #     # event.delete()
    # except Event.DoesNotExist:
    #     return JsonResponse({"success": False})
    return JsonResponse({"success": True})


def edit_member(request, member_pk):
    """View Member
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {}

    return render(request, 'member/edit.html', context)


def list_members(request):
    """List members
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {}

    return render(request, 'member/list.html', context)
