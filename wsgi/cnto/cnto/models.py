from django.db import models
from django.db.models.fields import DateTimeField


class Rank(models.Model):
    name = models.TextField(null=False)


class MemberGroup(models.Model):
    name = models.TextField(null=False)


class Member(models.Model):
    name = models.TextField(null=False)
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
        average_attendance = sum([attendance.attendance for attendance in attendances]) / len(attendances)

        return {"duration_minutes": event.duration_minutes, "average_attendance": average_attendance,
                "player_count": len(attendances)}

    event = models.ForeignKey(Event, null=False)
    member = models.ForeignKey(Member, null=False)
    attendance = models.FloatField(null=False)

    class Meta:
        unique_together = ('event', 'member',)