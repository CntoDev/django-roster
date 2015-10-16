from django.db import models
from django.db.models.fields import DateTimeField


class Rank(models.Model):
    name = models.TextField(null=False)


class MemberGroup(models.Model):
    name = models.TextField(null=False)


class Member(models.Model):
    name = models.TextField(null=False, unique=True)
    rank = models.ForeignKey(Rank, null=False)
    member_group = models.ForeignKey(MemberGroup, null=True)


class Event(models.Model):
    name = models.TextField()
    start_dt = DateTimeField(null=False)
    end_dt = DateTimeField(null=False)
    duration_minutes = models.IntegerField(null=False)


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