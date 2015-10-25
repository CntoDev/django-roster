from django.shortcuts import render, redirect
from django.utils import timezone
from cnto.templatetags.cnto_tags import has_permission
from ..models import Member, MemberGroup, EventType, Absence


def management(request):
    """List members
    """

    if not request.user.is_authenticated():
        return redirect("login")

    current_dt = timezone.now()

    recruits = sorted(Member.recruits(), key=lambda x: x.name.lower())
    discharges = sorted(Member.objects.all().filter(discharged=True, deleted=False), key=lambda x: x.name.lower())

    members = []
    if has_permission(request.user, "cnto_edit_members"):
        members = sorted(Member.active_members(), key=lambda x: x.name.lower())

    absentees = []
    if has_permission(request.user, "cnto_view_absentees"):
        absentees = sorted(
                Absence.objects.all().filter(concluded=False, deleted=False),
                key=lambda x: x.end_dt)

    groups = []
    if has_permission(request.user, "cnto_edit_groups"):
        groups = sorted(MemberGroup.objects.all(), key=lambda x: x.name.lower())

    event_types = []
    if has_permission(request.user, "cnto_edit_event_types"):
        event_types = sorted(EventType.objects.all(), key=lambda x: x.name.lower())

    context = {
        "members": members,
        "recruits": recruits,
        "current_absences": absentees,
        "discharges": discharges,
        "groups": groups,
        "event_types": event_types
    }

    return render(request, 'cnto/manage/main.html', context)


def home(request):
    return redirect("manage")
