from django.core.urlresolvers import reverse
from django.db import models


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

    def get_absolute_url(self):
        return reverse('edit-member', kwargs={'pk': self.pk})

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
    name = models.TextField()
    event_type = models.ForeignKey(EventType, null=False)
    start_dt = models.DateTimeField(null=False)
    end_dt = models.DateTimeField(null=False)
    duration_minutes = models.IntegerField(null=False)

    def lowered_name(self):
        return self.name.lower()


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

    def was_adequate(self):
        attendance_minutes = self.event.duration_minutes * self.attendance
        base_required_attendance_minutes = 60
        scaled_half_required_attendance_minutes = self.event.duration_minutes * 0.5

        return attendance_minutes > min(base_required_attendance_minutes, scaled_half_required_attendance_minutes)
