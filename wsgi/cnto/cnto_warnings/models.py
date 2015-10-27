import calendar

from django.db import models
from django.utils import timezone
from datetime import datetime
from cnto.models import Event, Member, CreatedModifiedMixin, Attendance


class LowAttendanceWarning(CreatedModifiedMixin):
    period_start_dt = models.DateTimeField(verbose_name="Period start date", null=False, default=timezone.now)
    period_end_dt = models.DateTimeField(verbose_name="Period end date", null=False, default=timezone.now)

    member = models.ForeignKey(Member, null=False)
    message = models.TextField(null=False)
    acknowledged = models.BooleanField(default=False)

    @staticmethod
    def add_and_update_warnings_for_month(month_dt):
        """

        :param month_dt:
        :return:
        """
        start_dt = datetime(month_dt.year, month_dt.month, 1, 0, 0)
        end_dt = datetime(month_dt.year, month_dt.month,
                          calendar.monthrange(month_dt.year, month_dt.month)[1], 23, 59)

        events = Event.all_for_time_period(start_dt, end_dt)

        members = Member.active_members(include_recruits=True)

        for member in members:
            adequate, reason = Attendance.was_adequate_for_period(member, events, start_dt, end_dt)

            # Check if the warning exists
            try:
                warning = LowAttendanceWarning.objects.get(period_start_dt=start_dt, period_end_dt=end_dt,
                                                           member=member)
                if not adequate:
                    if warning.message != reason:
                        warning.message = reason
                        warning.save()
                else:
                    warning.delete()
            except LowAttendanceWarning.DoesNotExist:
                if not adequate:
                    warning = LowAttendanceWarning(period_start_dt=start_dt, period_end_dt=end_dt, member=member,
                                                   message=reason)
                    warning.save()
