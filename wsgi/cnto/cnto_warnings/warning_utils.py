import calendar
from datetime import timedelta

from django.contrib.auth.models import User

from django.utils.timezone import datetime

from django.utils import timezone

from cnto.models import Member, Event, Attendance, Absence, Rank
from cnto_contributions.models import Contribution
from cnto_warnings.models import MemberWarning, MemberWarningType
from sens_do_not_commit import SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, SMTP_TLS_PORT, NOTIFICATION_EMAIL_ADDRESS, \
    NOTIFICATION_EMAIL_SUBJECT_LEAD
from utils.emailer import Emailer


def send_exception_email(exception_message):
    """

    :param exception_message:
    :return:
    """
    emailer = Emailer(host=SMTP_HOST, login_username=SMTP_USERNAME, login_password=SMTP_PASSWORD,
                      tls_port=SMTP_TLS_PORT)
    emailer.send_message(User.objects.get(username__iexact="admin").email, NOTIFICATION_EMAIL_ADDRESS,
                         NOTIFICATION_EMAIL_SUBJECT_LEAD + " exception",
                         exception_message)


def warning_exists(member, warning_type, message):
    """

    :return:
    """
    try:
        MemberWarning.objects.get(member=member, warning_type=warning_type, message=message)
        return True
    except MemberWarning.DoesNotExist:
        return False


def create_or_update_warning(member, warning_type, warning_active, message):
    """

    :param member:
    :param warning_type:
    :param warning_active:
    :param message:
    :return:
    """
    if warning_exists(member, warning_type, message):
        warning = MemberWarning.objects.get(member=member, warning_type=warning_type, message=message)
        if not warning_active:
            warning.delete()
    else:
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


def send_warning_emails():
    """

    :return:
    """
    emailer = Emailer(host=SMTP_HOST, login_username=SMTP_USERNAME, login_password=SMTP_PASSWORD,
                      tls_port=SMTP_TLS_PORT)

    warnings = MemberWarning.objects.filter(notified=False, acknowledged=False)

    for warning in warnings:
        recipients_string = warning.get_recipients_string()

        if recipients_string is None:
            continue

        subject, body = warning.get_subject_and_body()

        if subject is None or body is None:
            continue

        emailer.send_message(recipients_string, NOTIFICATION_EMAIL_ADDRESS,
                             NOTIFICATION_EMAIL_SUBJECT_LEAD + " %s" % (subject,),
                             body)

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


def add_absence_monitoring_warnings():
    """

    :return:
    """
    absence_starting_type = MemberWarningType.objects.get(name__iexact="Absence Starting")
    absence_ending_type = MemberWarningType.objects.get(name__iexact="Absence Ending")
    absence_violated_type = MemberWarningType.objects.get(name__iexact="Absence Violated")

    absences = Absence.objects.filter(concluded=False, deleted=False)
    for absence in absences:
        # If the absence doesn't begin that day, it would be useful if notification would appear on warning tab and
        # email on the date when the absence actually begin; i.e. absence start date, with text:
        # "NAME's abesence begin today, please assign him the appropriate tag."
        if absence.start_date == timezone.now().date():
            create_or_update_warning(absence.member, absence_starting_type,
                                     True, "%s's absence begins on %s, please assign him the appropriate tag." % (
                                         absence.member.name, absence.start_date.strftime("%Y-%m-%d")))

        # It would be very useful if we could have notification appear on the warning tab, a day after user's absence
        #  has ended, along with the email with the text:
        # "NAME's absence tag has ended on "DATE. Send him the stationary PM."
        if absence.end_date == (timezone.now() - timedelta(days=1)).date():
            create_or_update_warning(absence.member, absence_ending_type,
                                     True, "%s's absence tag has ended on %s. Send him the stationary PM." % (
                                         absence.member.name, absence.end_date.strftime("%Y-%m-%d")))

        # If the absence hasn't been concluded within 15 days of the expiration date, a new notification should
        # appear on the warning tab along with email with the text:
        # "NAME didn't reply to the stationary PM within two weeks of the PM."
        if absence.end_date == (timezone.now() - timedelta(days=15)).date():
            create_or_update_warning(absence.member, absence_violated_type,
                                     True,
                                     "%s didn't reply to the stationary PM within two weeks of the ending date %s." % (
                                         absence.member.name, absence.end_date.strftime("%Y-%m-%d")))


def add_and_update_contribution_about_to_expire():
    """

    :return:
    """
    relevant_expiry_date = timezone.now() + timedelta(days=14)
    contribution_expiry_warning_type = MemberWarningType.objects.get(name__iexact="Contribution Expiring")
    expiring_contributions = Contribution.objects.filter(end_date=relevant_expiry_date)

    for contribution in expiring_contributions:
        create_or_update_warning(contribution.member, contribution_expiry_warning_type,
                                 True, "%s's %s contributor tag will run out at %s. Send him the stationary PM." % (
                                     contribution.member.name, contribution.type.name,
                                     contribution.end_date.strftime("%Y-%m-%d")))


def add_and_update_low_attendances_for_cycle(cycle_start_dt):
    """

    :param month_dt:
    :return:
    """
    low_attendance_warning_type = MemberWarningType.objects.get(name__iexact="Low Attendance")
    start_dt, end_dt = calculate_start_and_end_dt_for_cycle(cycle_start_dt)

    events = Event.all_for_time_period(start_dt, end_dt)

    members = Member.active_members(include_recruits=True)

    for member in members:
        adequate, message = Attendance.was_adequate_for_period(member, events, start_dt, end_dt, ignore_absences=False)

        create_or_update_warning(member, low_attendance_warning_type, not adequate, message)


def allocate_ranks_and_add_warnings_for_cycle(cycle_start_dt):
    start_dt, end_dt = calculate_start_and_end_dt_for_cycle(cycle_start_dt)

    gnt_demoted_warning_type = MemberWarningType.objects.get(name__iexact="Grunt Demoted")
    res_promoted_warning_type = MemberWarningType.objects.get(name__iexact="Reservist Promoted")

    events = Event.all_for_time_period(start_dt, end_dt)
    event_count = events.count()
    min_gnt_event_count = round(float(event_count) / 3.0)

    members = Member.active_members(include_recruits=True)
    gnt_rank = Rank.objects.get(name__iexact="gnt")
    res_rank = Rank.objects.get(name__iexact="res")

    for member in members:
        member_rank = member.rank

        if member_rank != gnt_rank and member_rank != res_rank:
            # Other ranks are not subject to attendance restrictions
            continue

        gnt_adequate, message = Attendance.was_adequate_for_period(member, events, start_dt, end_dt,
                                                                   min_total_events=min_gnt_event_count)

        if member_rank == res_rank and gnt_adequate:
            rank_message = "%s has been promoted to Grunt due to attending at least %s events between %s and %s." % (
                member.name, min_gnt_event_count, start_dt.strftime("%Y-%m-%d"),
                end_dt.strftime("%Y-%m-%d"))

            if warning_exists(member, res_promoted_warning_type, rank_message):
                continue

            # Promote to grunt
            member.rank = gnt_rank
            member.save()

            create_or_update_warning(member, res_promoted_warning_type, True,
                                     rank_message)

        elif member_rank == gnt_rank and not gnt_adequate:
            rank_message = "%s has been demoted to Reservist due to attending less than %s events between %s and %s." \
                           % (member.name, min_gnt_event_count, start_dt.strftime("%Y-%m-%d"),
                              end_dt.strftime("%Y-%m-%d"))

            if warning_exists(member, gnt_demoted_warning_type, rank_message):
                continue

            # Demote to reservist
            member.rank = res_rank
            member.save()

            create_or_update_warning(member, gnt_demoted_warning_type, True,
                                     rank_message)


def allocate_ranks_and_add_warnings_for_previous_cycle():
    previous_cycle_start_dt = calculate_previous_cycle_start_dt()

    allocate_ranks_and_add_warnings_for_cycle(previous_cycle_start_dt)


def calculate_previous_cycle_start_dt():
    current_dt = timezone.now()
    previous_year_number = current_dt.year
    previous_month_number = current_dt.month - 2

    if previous_month_number < 1:
        previous_month_number = 11
        previous_year_number -= 1

    if previous_month_number % 2 == 0:
        previous_month_number -= 1

    previous_cycle_start_dt = datetime(previous_year_number, previous_month_number, 1, 0, 0)
    return previous_cycle_start_dt


def calculate_start_and_end_dt_for_cycle(month_dt):
    start_dt = timezone.make_aware(datetime(month_dt.year, month_dt.month, 1, 0, 0),
                                   timezone.get_default_timezone())
    cycle_end_month_number = month_dt.month + 1
    end_dt = timezone.make_aware(datetime(month_dt.year, cycle_end_month_number,
                                          calendar.monthrange(month_dt.year, cycle_end_month_number)[1], 23, 59),
                                 timezone.get_default_timezone())

    return start_dt, end_dt


def add_and_update_low_attendance_for_previous_cycle():
    """

    :return:
    """
    previous_cycle_start_dt = calculate_previous_cycle_start_dt()

    add_and_update_low_attendances_for_cycle(previous_cycle_start_dt)
