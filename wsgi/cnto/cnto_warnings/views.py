from django.shortcuts import render, redirect


# Create your views here.
from cnto.templatetags.cnto_tags import has_permission
from cnto_warnings.models import MemberWarning


def list_warnings(request):
    """Browse reports
    """

    if not request.user.is_authenticated():
        return redirect("login")
    elif not has_permission(request.user, "cnto_view_reports"):
        return redirect("manage")

    context = {
        "warnings": MemberWarning.objects.all()
    }

    return render(request, 'cnto_warnings/list.html', context)
