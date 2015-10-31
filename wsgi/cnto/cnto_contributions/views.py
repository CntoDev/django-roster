from datetime import timedelta
from django.http.response import JsonResponse, Http404
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from django.utils import timezone
from cnto.models import Member
from cnto.templatetags.cnto_tags import has_permission
from cnto_contributions.forms import ContributionForm
from cnto_contributions.models import Contribution


def delete_contribution(request, contribution_pk):
    """Return the daily process main overview page.
    """

    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_edit_contributions"):
        return redirect("manage")

    try:
        contribution = Contribution.objects.get(pk=contribution_pk)
        contribution.delete()
        return JsonResponse({"success": True})
    except Contribution.DoesNotExist:
        return JsonResponse({"success": False})


def handle_contribution_change_view(request, edit_mode, contribution):
    if request.POST:
        form = ContributionForm(request.POST, instance=contribution)
        if request.POST.get("cancel"):
            return redirect('edit-contributions-for-member', contribution.member.pk)
        elif form.is_valid():
            form.save()
            return redirect('edit-contributions-for-member', contribution.member.pk)
    else:
        contribution.start_date = timezone.now().date()
        contribution.end_date = (timezone.now() + timedelta(days=30 * 6)).date()

        form = ContributionForm(instance=contribution)

    context = {}
    context.update(csrf(request))

    context['form'] = form
    context["edit_mode"] = edit_mode
    context["member"] = contribution.member

    return render_to_response('cnto_contributions/edit.html', context)


def create_contribution(request, member_pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_edit_contributions"):
        return redirect("manage")

    try:
        member = Member.objects.get(pk=member_pk)
    except Member.DoesNotExist:
        raise Http404()

    contribution = Contribution(member=member)

    return handle_contribution_change_view(request, edit_mode=False, contribution=contribution)


def edit_contribution(request, contribution_pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_edit_contributions"):
        return redirect("manage")

    try:
        contribution = Contribution.objects.get(pk=contribution_pk)
    except Contribution.DoesNotExist:
        raise Http404()

    return handle_contribution_change_view(request, edit_mode=True, contribution=contribution)


def edit_for_member(request, member_pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_edit_contributions"):
        return redirect("manage")

    try:
        member = Member.objects.get(pk=member_pk)
    except Member.DoesNotExist:
        raise Http404()

    context = {
        "member": member,
        "contributions": sorted(Contribution.objects.filter(member=member), key=lambda x: x.end_date,
                                reverse=True),
    }

    return render(request, 'cnto_contributions/list-for-member.html', context)
