from braces.views import JSONResponseMixin
from django.http.response import JsonResponse, Http404
from django.shortcuts import render, redirect


# Create your views here.
from cnto.models import Member
from cnto.templatetags.cnto_tags import has_permission
from cnto_warnings.models import MemberWarning


def toggle_member_acknowledge(request, pk):
    """Browse reports
    """

    success = True
    if not request.user.is_authenticated():
        success = False
    elif not has_permission(request.user, "cnto_view_reports"):
        success = False
    else:
        try:
            warning = MemberWarning.objects.get(pk=pk)
            if warning.acknowledged:
                warning.acknowledged = False
            else:
                warning.acknowledged = True
            warning.save()
        except MemberWarning.DoesNotExist:
            success = False

    return JsonResponse({
        "success": success
    })


def list_warnings(request):
    """Browse reports
    """

    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_view_reports"):
        return redirect("manage")

    context = {
        "warnings": MemberWarning.objects.filter(acknowledged=False),
        "warning_count": MemberWarning.objects.filter(acknowledged=False).count()
    }

    return render(request, 'cnto_warnings/list.html', context)


def list_warnings_for_member(request, member_pk):
    """Browse reports
    """

    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_view_reports"):
        return redirect("manage")

    try:
        member = Member.objects.get(pk=member_pk)
    except Member.DoesNotExist:
        raise Http404()

    context = {
        "member": member,
        "warnings": MemberWarning.objects.filter(member=member)
    }

    return render(request, 'cnto_warnings/list-for-member.html', context)
