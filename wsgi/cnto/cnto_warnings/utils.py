import calendar
from django.utils.timezone import datetime
from django.utils import timezone
from cnto.models import Member, Event, Attendance
from cnto_warnings.models import MemberWarning, MemberWarningType


def create_or_update_warning(member, warning_type, warning_active, message):
    """

    :param member:
    :param warning_type:
    :param warning_active:
    :param message:
    :return:
    """
    try:
        warning = MemberWarning.objects.get(member=member, warning_type=warning_type, message=message)
        if not warning_active:
            warning.delete()
    except MemberWarning.DoesNotExist:
        if warning_active:
            warning = MemberWarning(member=member, warning_type=warning_type, message=message)
            warning.save()


def add_and_update_mod_assessment_due():
    """

    :return:
    """
    mod_assessment_due_warning_type = MemberWarningType.objects.get(name__iexact="Mod Assessment Due")
    recruits = Member.recruits()

    for member in recruits:
        mod_assessment_due, message = member.is_mod_assessment_due()
        create_or_update_warning(member, mod_assessment_due_warning_type, mod_assessment_due, message)


def add_and_update_grunt_qualification_due():
    """

    :return:
    """
    grunt_qualification_due_warning_type = MemberWarningType.objects.get(name__iexact="Grunt Qualification Due")
    recruits = Member.recruits()

    for member in recruits:
        grunt_qualification_due, message = member.is_grunt_qualification_due()
        create_or_update_warning(member, grunt_qualification_due_warning_type, grunt_qualification_due, message)


def add_and_update_low_attendances_for_month(month_dt):
    """

    :param month_dt:
    :return:
    """
    low_attendance_warning_type = MemberWarningType.objects.get(name__iexact="Low Attendance")
    start_dt = timezone.make_aware(datetime(month_dt.year, month_dt.month, 1, 0, 0),
                                   timezone.get_default_timezone())
    end_dt = timezone.make_aware(datetime(month_dt.year, month_dt.month,
                                          calendar.monthrange(month_dt.year, month_dt.month)[1], 23, 59),
                                 timezone.get_default_timezone())

    events = Event.all_for_time_period(start_dt, end_dt)

    members = Member.active_members(include_recruits=True)

    for member in members:
        adequate, message = Attendance.was_adequate_for_period(member, events, start_dt, end_dt)

        create_or_update_warning(member, low_attendance_warning_type, not adequate, message)


def add_and_update_low_attendace_for_previous_month():
    """

    :return:
    """
    current_dt = timezone.now()
    previous_year_number = current_dt.year
    previous_month_number = current_dt.month - 1

    if previous_month_number < 1:
        previous_month_number = 12
        previous_year_number -= 1

    previous_month_start_dt = datetime(previous_year_number, previous_month_number, 1, 0, 0)

    add_and_update_low_attendances_for_month(previous_month_start_dt)
