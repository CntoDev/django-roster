import calendar
from django.contrib.auth.models import User
from django.utils.timezone import datetime
from django.utils import timezone
from cnto.models import Member, Event, Attendance
from cnto_warnings.models import MemberWarning, MemberWarningType
from sens_do_not_commit import SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, SMTP_TLS_PORT, NOTIFICATION_EMAIL_ADDRESS, \
    NOTIFICATION_EMAIL_SUBJECT_LEAD
from utils.emailer import Emailer


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


def recipients_to_recipient_string(recipient_users):
    """

    :param recipient_users:
    :return:
    """
    recipient_emails = []
    for recipient in recipient_users:
        if len(recipient.email) > 0:
            recipient_emails.append(recipient.email)

    if len(recipient_emails) == 0:
        return None
    else:
        return ";".join(recipient_emails)


def send_warning_emails():
    """

    :return:
    """
    emailer = Emailer(host=SMTP_HOST, login_username=SMTP_USERNAME, login_password=SMTP_PASSWORD,
                      tls_port=SMTP_TLS_PORT)

    # Mod assessment emails
    mod_warning_type = MemberWarningType.objects.get(name__iexact="Mod Assessment Due")
    mod_warnings = MemberWarning.objects.filter(warning_type=mod_warning_type, notified=False, acknowledged=False)

    for warning in mod_warnings:
        recipient_users = [
            User.objects.get(name__iexact="admin"),
            User.objects.get(name__iexact="abuk"),
            User.objects.get(name__iexact="john"),
        ]
        recipient_string = recipients_to_recipient_string(recipient_users)
        if recipient_string is not None:
            emailer.send_message(recipient_string, NOTIFICATION_EMAIL_ADDRESS,
                                 NOTIFICATION_EMAIL_SUBJECT_LEAD + " Mod assessment for %s overdue" % (
                                     warning.member.name,),
                                 "%s didn't report to have his mods assessed within two weeks of joining our community." % (warning.member.name,))

            warning.notified = True
            warning.save()

    # Grunt qualification emails
    grunt_warning_type = MemberWarningType.objects.get(name__iexact="Grunt Qualification Due")
    grunt_warnings = MemberWarning.objects.filter(warning_type=grunt_warning_type, notified=False, acknowledged=False)

    for warning in grunt_warnings:
        recipient_users = [
            User.objects.get(name__iexact="admin"),
            User.objects.get(name__iexact="abuk"),
            User.objects.get(name__iexact="john"),
        ]
        recipient_string = recipients_to_recipient_string(recipient_users)
        if recipient_string is not None:
            emailer.send_message(recipient_string, NOTIFICATION_EMAIL_ADDRESS,
                                 NOTIFICATION_EMAIL_SUBJECT_LEAD + " Grunt Qualification for %s overdue" % (
                                     warning.member.name,),
                                 "%s didn't qualify to become a Grunt within 6 weeks of joining our community." % (
                                     warning.member.name,))
            warning.notified = True
            warning.save()


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
