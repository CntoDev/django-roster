from django.shortcuts import render, redirect
from django.utils import timezone
from ..models import Member, MemberGroup, EventType, Absence


def management(request):
    """List members
    """

    if not request.user.is_authenticated():
        return redirect("login")

    current_dt = timezone.now()

    context = {
        "members": sorted(Member.active_members(),
                          key=lambda x: x.name.lower()),
        "current_absences": sorted(
            Absence.objects.all().filter(start_dt__lt=current_dt, end_dt__gt=current_dt, deleted=False),
            key=lambda x: x.end_dt),
        "discharges": sorted(Member.objects.all().filter(discharged=True, deleted=False), key=lambda x: x.name.lower()),
        "groups": sorted(MemberGroup.objects.all(), key=lambda x: x.name.lower()),
        "event_types": sorted(EventType.objects.all(), key=lambda x: x.name.lower())
    }

    return render(request, 'cnto/manage/main.html', context)
