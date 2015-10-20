from datetime import datetime
from django.http.response import JsonResponse

from django.http import Http404
from django.shortcuts import redirect, render_to_response
from django.template.context_processors import csrf
from ..models import Member, Rank
from ..forms import MemberForm, DischargedMemberForm


def delete_member(request, member_pk):
    """Delete Member
    """

    if not request.user.is_authenticated():
        return redirect("login")

    try:
        member = Member.objects.get(pk=member_pk)
        member.deleted = True
        member.save()
    except Member.DoesNotExist:
        return JsonResponse({"success": False})
    return JsonResponse({"success": True})


def handle_member_change_view(request, edit_mode=False, member=None):
    if request.POST:
        form = MemberForm(request.POST, instance=member)
        if request.POST.get("cancel"):
            return redirect('list-members')
        elif form.is_valid():
            if form.cleaned_data["rank"] is None:
                try:
                    rec_rank = Rank.objects.get(name__iexact="Rec")
                except Rank.DoesNotExist:
                    rec_rank = Rank(name="Rec")
                    rec_rank.save()

                form.cleaned_data["rank"] = rec_rank

            if form.cleaned_data["discharged"] and form.cleaned_data["discharge_dt"] is None:
                form.instance.discharge_dt = datetime.now()

            form.save()
            return redirect('list-members')
    else:
        if member is None:
            try:
                rec_rank = Rank.objects.get(name__iexact="Rec")
            except Rank.DoesNotExist:
                rec_rank = Rank(name="Rec")
                rec_rank.save()

            initial = {
                'rank': rec_rank,
                'mods_assessed': False
            }
            form = MemberForm(initial=initial)
        else:
            form = MemberForm(instance=member)

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args["edit_mode"] = edit_mode

    return render_to_response('cnto/member/edit.html', args)


def handle_discharged_member_change_view(request, member):
    if request.POST:
        form = DischargedMemberForm(request.POST, instance=member)
        if request.POST.get("cancel"):
            return redirect('list-members')
        elif form.is_valid():
            if not form.cleaned_data["discharged"]:
                form.instance.discharge_dt = None

            form.save()
            return redirect('list-members')
    else:
        form = DischargedMemberForm(instance=member)

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('cnto/member/edit-discharged.html', args)


def create_member(request):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    return handle_member_change_view(request)


def edit_discharged_member(request, pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        raise Http404()

    return handle_discharged_member_change_view(request, member=member)


def edit_member(request, pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        raise Http404()

    return handle_member_change_view(request, edit_mode=True, member=member)
