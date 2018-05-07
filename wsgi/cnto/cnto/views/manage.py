from django.db import models
from django.shortcuts import render, redirect
from django.utils import timezone
from cnto.templatetags.cnto_tags import has_permission
from cnto_contributions.models import Contribution
from cnto_warnings.models import MemberWarning
from cnto_notes.models import Note
from ..models import Member, MemberGroup, EventType, Absence, Attendance


def management(request):
    """List members
    """

    if not request.user.is_authenticated():
        return redirect("login")

    if not has_permission(request.user, "cnto_edit_members") and not has_permission(request.user, "cnto_view_absentees"):
        return redirect("report-main")

    recruits = Member.recruits().order_by('name').select_related(
            'rank',
            'member_group',
    ).prefetch_related(
            models.Prefetch('attendances', queryset=Attendance.objects.all().select_related(
                'event',
                'event__event_type',
            )),
            models.Prefetch('notes', queryset=Note.objects.order_by('-id')),
    )
    discharges = Member.objects.all().filter(discharged=True, deleted=False).order_by('name').select_related(
            'rank',
            'member_group',
    ).prefetch_related(
            models.Prefetch('notes', queryset=Note.objects.order_by('-id')),
    )

    members = []
    if has_permission(request.user, "cnto_edit_members"):
        members = Member.active_members().order_by('name').select_related(
            'rank',
            'member_group',
        ).prefetch_related(
            models.Prefetch('notes', queryset=Note.objects.order_by('-id')),
        )

    absentees = []
    if has_permission(request.user, "cnto_view_absentees"):
        absentees = Absence.objects.all().filter(
            member__discharged=False,
            concluded=False,
            deleted=False,
        ).order_by('end_date').select_related(
            'absence_type',
            'member',
            'member__member_group',
        )

    groups = []
    if has_permission(request.user, "cnto_edit_groups"):
        groups = MemberGroup.objects.all().order_by('name')

    event_types = []
    if has_permission(request.user, "cnto_edit_event_types"):
        event_types = EventType.objects.all().order_by('name')

    active_contributions = []
    if has_permission(request.user, "cnto_edit_contributions"):
        active_contributions = Contribution.objects.filter(
            end_date__gte=timezone.now().date(),
        ).order_by('end_date').select_related(
            'type',
            'member',
        )
    context = {
        "members": members,
        "recruits": recruits,
        "current_absences": absentees,
        "discharges": discharges,
        "groups": groups,
        "active_contributions": active_contributions,
        "event_types": event_types,
        "warning_count": MemberWarning.objects.filter(acknowledged=False).count()
    }

    return render(request, 'cnto/manage/main.html', context)


def home(request):
    return redirect("manage")
