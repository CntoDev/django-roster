from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Rank(models.Model):
    name = models.TextField(null=False, unique=True)

    def __str__(self):
        return self.name

    def lowered_name(self):
        return self.name.lower()


class MemberGroup(models.Model):
    name = models.TextField(null=False, unique=True)

    def __str__(self):
        return self.name

    def lowered_name(self):
        return self.name.lower()


class Member(models.Model):
    name = models.TextField(null=False, unique=True)
    rank = models.ForeignKey(Rank, null=False)
    member_group = models.ForeignKey(MemberGroup, null=True)
    email = models.EmailField(null=True)

    join_dt = models.DateTimeField(verbose_name="Join date", null=False, default=timezone.now)

    discharged = models.BooleanField(default=False, null=False)
    discharge_dt = models.DateTimeField(verbose_name="Discharge date", null=True, default=None)

    mods_assessed = models.BooleanField(default=True, null=False)
    deleted = models.BooleanField(default=False, null=False)

    @staticmethod
    def active_members():
        return Member.objects.all().filter(deleted=False, discharged=False)

    def get_absolute_url(self):
        return reverse('edit-member', kwargs={'pk': self.pk})

    def get_recruit_warning(self):
        if "rec" not in self.rank.name.lower():
            return False, "Not recruit."

        current_dt = timezone.now()
        if self.join_dt < current_dt - timedelta(days=42):
            # Six weeks grunt notice
            return True, "Has not qualified as grunt in required time period.  Member since %s." % (
                self.join_dt.strftime("%Y-%m-%d"), )
        if self.join_dt < current_dt - timedelta(days=14) and not self.mods_assessed:
            # Two weeks mod assessment
            return True, "Has not assessed mods in required time period.  Member since %s." % (
                self.join_dt.strftime("%Y-%m-%d"), )

        return False, "No warnings."


    def __str__(self):
        return self.name

    def lowered_name(self):
        return self.name.lower()


class EventType(models.Model):
    name = models.TextField(null=False)
    default_start_hour = models.IntegerField()
    default_end_hour = models.IntegerField()
    css_class_name = models.TextField(null=False, blank=True)

    def lowered_name(self):
        return self.name.lower()


class Event(models.Model):
    @staticmethod
    def all_for_time_period(start_dt, end_dt):
        return Event.objects.filter(start_dt__gte=start_dt, start_dt__lte=end_dt)

    name = models.TextField()
    event_type = models.ForeignKey(EventType, null=False)
    start_dt = models.DateTimeField(null=False)
    end_dt = models.DateTimeField(null=False)
    duration_minutes = models.IntegerField(null=False)

    def lowered_name(self):
        return self.name.lower()


class AbsenceType(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class Absence(models.Model):
    member = models.ForeignKey(Member, null=False)
    absence_type = models.ForeignKey(AbsenceType, null=False)
    start_dt = models.DateTimeField(null=False)
    end_dt = models.DateTimeField(null=False)
    deleted = models.BooleanField(default=False, null=False)

    def due_days(self):
        return (self.end_dt - timezone.now()).days


class Attendance(models.Model):
    @staticmethod
    def get_stats_for_event(event):
        """

        :param event:
        :return:
        """
        attendances = Attendance.objects.filter(event=event)
        if len(attendances) > 0:
            average_attendance = sum([attendance.attendance for attendance in attendances]) / len(attendances)
        else:
            average_attendance = 0

        return {"duration_minutes": event.duration_minutes, "average_attendance": average_attendance,
                "player_count": len(attendances)}

    event = models.ForeignKey(Event, null=False)
    member = models.ForeignKey(Member, null=False)
    attendance = models.FloatField(null=False)

    class Meta:
        unique_together = ('event', 'member',)

    @staticmethod
    def was_adequate_for_period(member, events, start_dt, end_dt):
        if member.join_dt > start_dt:
            return True, "Was not a member for entire period."

        start_absences_for_period = Absence.objects.filter(member=member, start_dt__lte=start_dt, end_dt__gte=start_dt)
        end_absences_for_period = Absence.objects.filter(member=member, start_dt__lte=end_dt, end_dt__gte=end_dt)
        inside_absences_for_period = Absence.objects.filter(member=member, start_dt__gte=start_dt, end_dt__lte=end_dt)
        overlap_absences_for_period = Absence.objects.filter(member=member, start_dt__lte=start_dt, end_dt__gte=end_dt)

        if start_absences_for_period.count() + end_absences_for_period.count() + inside_absences_for_period.count() + overlap_absences_for_period.count() > 0:
            return True, "Was marked absent during period."

        attendances_for_period = Attendance.objects.filter(member=member, event__in=events)

        attended_training = 0
        attended_other = 0

        training_event_type = EventType.objects.get(name__iexact="training")

        for attendance in attendances_for_period:
            if attendance.was_adequate():
                if attendance.event.event_type == training_event_type:
                    attended_training += 1
                else:
                    attended_other += 1

        attended_total = attended_training + attended_other

        min_total_events = 3
        min_trainings = 1

        between_string = "between %s and %s" % (start_dt.strftime("%Y-%m-%d"), end_dt.strftime("%Y-%m-%d"))

        if attended_total < min_total_events:
            return False, "Did not attend enough events %s (%s < %s)." % (
                between_string, attended_total, min_total_events)
        if attended_training < min_trainings:
            return False, "Did not attend enough trainings %s (%s < %s)." % (
                between_string, attended_training, min_trainings)
        if attended_other < min_total_events - min_trainings:
            return False, "Did not attend enough non-training events %s (%s < %s)." % (
                between_string, attended_other, min_total_events - min_trainings)

        return True, "No attendance issues."

    def was_adequate(self):
        attendance_minutes = self.event.duration_minutes * self.attendance
        base_required_attendance_minutes = 60
        scaled_half_required_attendance_minutes = self.event.duration_minutes * 0.5

        return attendance_minutes > min(base_required_attendance_minutes, scaled_half_required_attendance_minutes)
