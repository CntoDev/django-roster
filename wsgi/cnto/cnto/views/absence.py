from django.utils import timezone
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from ..models import Member, MemberGroup, Absence
from ..forms import AbsenceForm
from django.http import Http404
from django.template.context_processors import csrf


def delete_absence(request, absence_pk):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")

    try:
        absence = Absence.objects.get(pk=absence_pk)
        absence.deleted = True
        absence.save()
        return JsonResponse({"success": True})
    except Absence.DoesNotExist:
        return JsonResponse({"success": False})


def handle_absence_change_view(request, edit_mode, absence):
    if request.POST:
        form = AbsenceForm(request.POST, instance=absence)
        if request.POST.get("cancel"):
            return redirect('edit-absences', absence.member.pk)
        elif form.is_valid():
            form.save()
            return redirect('edit-absences', absence.member.pk)
    else:
        form = AbsenceForm(instance=absence)

    context = {}
    context.update(csrf(request))

    context['form'] = form
    context["edit_mode"] = edit_mode
    context["member"] = absence.member

    return render_to_response('cnto/absence/edit.html', context)


def create_absence(request, member_pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    try:
        member = Member.objects.get(pk=member_pk)
    except Member.DoesNotExist:
        raise Http404()

    absence = Absence(member=member)

    return handle_absence_change_view(request, edit_mode=False, absence=absence)


def edit_absence(request, absence_pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    try:
        absence = Absence.objects.get(pk=absence_pk)
    except Absence.DoesNotExist:
        raise Http404()

    return handle_absence_change_view(request, edit_mode=True, absence=absence)


def edit_absences(request, member_pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    try:
        member = Member.objects.get(pk=member_pk)
    except Member.DoesNotExist:
        raise Http404()

    context = {
        "member": member,
        "absences": sorted(Absence.objects.filter(member=member, deleted=False), key=lambda x: x.start_date,
                           reverse=True),
    }

    return render(request, 'cnto/absence/list-for-member.html', context)
