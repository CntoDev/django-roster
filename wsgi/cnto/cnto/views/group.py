from django.http.response import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from ..models import Member, MemberGroup
from ..forms import MemberGroupForm
from django.http import Http404
from django.template.context_processors import csrf


def delete_group(request, pk):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

    try:
        group = MemberGroup.objects.get(pk=pk)
        group.delete()
        return JsonResponse({"success": True})
    except MemberGroup.DoesNotExist:
        return JsonResponse({"success": False})


def handle_group_change_view(request, edit_mode, group=None):
    if request.POST:
        form = MemberGroupForm(request.POST, instance=group)
        if request.POST.get("cancel"):
            return redirect('manage')
        elif form.is_valid():
            form.save()
            return redirect('manage')
    else:
        form = MemberGroupForm(instance=group)

    context = {}
    context.update(csrf(request))

    context['form'] = form
    context["edit_mode"] = edit_mode

    return render_to_response('cnto/group/edit.html', context)


def create_group(request):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    return handle_group_change_view(request, edit_mode=False)


def edit_group(request, pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    try:
        group = MemberGroup.objects.get(pk=pk)
    except MemberGroup.DoesNotExist:
        raise Http404()

    return handle_group_change_view(request, edit_mode=True, group=group)
