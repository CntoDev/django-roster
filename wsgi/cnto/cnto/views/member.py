from datetime import timedelta
from django.utils import timezone
from django.http.response import JsonResponse

from django.http import Http404
from django.shortcuts import redirect, render_to_response
from django.template.context_processors import csrf
from cnto import RECRUIT_RANK
from cnto.templatetags.cnto_tags import has_permission
from cnto_warnings.models import MemberWarning
from ..models import Member, Rank
from ..forms import MemberForm, DischargedMemberForm


def delete_member(request, member_pk):
    """Delete Member
    """

    if not request.user.is_authenticated():
        return redirect("login")

    try:
        member = Member.objects.get(pk=member_pk)

        if not has_permission(request.user, "cnto_edit_members"):
            if RECRUIT_RANK not in member.rank.name.lower():
                return redirect("manage")

        member.deleted = True
        member.save()
    except Member.DoesNotExist:
        return JsonResponse({"success": False})
    return JsonResponse({"success": True})


def handle_member_change_view(request, edit_mode=False, member=None, recruit_only=False):
    """

    :param request:
    :param edit_mode:
    :param member:
    :param recruit_only:
    :return:
    """
    rec_queryset = Rank.objects.filter(name__iexact="Rct")

    if request.POST:
        form = MemberForm(request.POST, instance=member)
        if recruit_only:
            form.fields["rank"].queryset = rec_queryset

        if request.POST.get("cancel"):
            return redirect('manage')
        elif form.is_valid():
            if form.cleaned_data["rank"] is None:
                try:
                    rec_rank = Rank.objects.get(name__iexact=RECRUIT_RANK)
                except Rank.DoesNotExist:
                    rec_rank = Rank(name=RECRUIT_RANK)
                    rec_rank.save()

                form.cleaned_data["rank"] = rec_rank

            if form.cleaned_data["discharged"]:
                if form.cleaned_data["discharge_date"] is None:
                    form.instance.discharge_date = timezone.now()

                form.instance.member_group = None

            form.save()
            return redirect('manage')
    else:
        if member is None:
            try:
                rec_rank = Rank.objects.get(name__iexact=RECRUIT_RANK)
            except Rank.DoesNotExist:
                rec_rank = Rank(name=RECRUIT_RANK)
                rec_rank.save()

            initial = {
                'rank': rec_rank,
                'mods_assessed': False,
                'bqf_assessed': False,
                'join_date': timezone.now().date()
            }
            form = MemberForm(initial=initial)
            if recruit_only:
                form.fields["rank"].queryset = rec_queryset
        else:
            form = MemberForm(instance=member)
            if recruit_only:
                form.fields["rank"].queryset = rec_queryset

    args = {}
    args.update(csrf(request))

    args["user"] = request.user
    args['form'] = form
    args["edit_mode"] = edit_mode
    args["warning_count"] = MemberWarning.objects.filter(acknowledged=False).count()

    return render_to_response('cnto/member/edit.html', args)


def handle_discharged_member_change_view(request, member):
    if request.POST:
        form = DischargedMemberForm(request.POST, instance=member)
        if request.POST.get("cancel"):
            return redirect('manage')
        elif form.is_valid():
            if not form.cleaned_data["discharged"]:
                form.instance.discharge_date = None

            form.save()
            return redirect('manage')
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
    elif not has_permission(request.user, "cnto_edit_members"):
        return redirect("manage")

    return handle_member_change_view(request)


def create_recruit(request):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    return handle_member_change_view(request, recruit_only=True)


def edit_discharged_member(request, pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        raise Http404()

    if not has_permission(request.user, "cnto_edit_members"):
        if RECRUIT_RANK not in member.rank.name.lower():
            return redirect("manage")

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

    if not has_permission(request.user, "cnto_edit_members"):
        if RECRUIT_RANK not in member.rank.name.lower():
            return redirect("manage")

        recruit_only = True
    else:
        recruit_only = False

    return handle_member_change_view(request, edit_mode=True, member=member, recruit_only=recruit_only)
