from django.http.response import JsonResponse, HttpResponseNotFound
from django.http import Http404
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from ..models import Member, MemberGroup, Rank
from ..forms import MemberForm


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


def handle_member_change_view(request, member=None):
    if request.POST:
        form = MemberForm(request.POST, instance=member)
        if request.POST.get("cancel"):
            return redirect('list-members')
        elif form.is_valid():
            if form.fields["rank"] is None:
                form.fields["rank"] = Rank.get_or_create_by_name("Rec")

            form.save()
            return redirect('list-members')
    else:
        form = MemberForm(instance=member)

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('member/edit.html', args)


def create_member(request):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    return handle_member_change_view(request)


def edit_member(request, pk):
    """View Member
    """
    if not request.user.is_authenticated():
        return redirect("login")

    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        raise Http404()

    return handle_member_change_view(request, member=member)


def list_members(request):
    """List members
    """

    if not request.user.is_authenticated():
        return redirect("login")

    context = {
        "members": sorted(Member.objects.all(), key=lambda x: x.name),
        "groups": sorted(MemberGroup.objects.all(), key=lambda x: x.name)
    }

    return render(request, 'member/list.html', context)
