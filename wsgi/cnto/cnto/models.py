from django.core.urlresolvers import reverse
from django.db import models


class Rank(models.Model):
    @staticmethod
    def get_or_create_by_name(name):
        used_name = name.lower()
        try:
            rank = Rank.objects.get(name=used_name)
        except Rank.DoesNotExist:
            rank = Rank.objects.create(name=used_name)

        return rank

    name = models.TextField(null=False, unique=True)

    def __str__(self):
        return self.name


class MemberGroup(models.Model):
    @staticmethod
    def get_or_create_by_name(name):
        used_name = name.lower()
        try:
            member_group = MemberGroup.objects.get(name=used_name)
        except MemberGroup.DoesNotExist:
            member_group = MemberGroup.objects.create(name=used_name)

        return member_group

    name = models.TextField(null=False, unique=True)

    def __str__(self):
        return self.name


class Member(models.Model):
    @staticmethod
    def get_or_create_by_username(username, rank=None):
        used_username = username.lower()
        try:
            member = Member.objects.get(name=used_username)
        except Member.DoesNotExist:
            if rank is not None:
                member = Member.objects.create(name=used_username, rank=rank)
            else:
                member = Member.objects.create(name=used_username)

        return member

    name = models.TextField(null=False, unique=True)
    rank = models.ForeignKey(Rank, null=False)
    member_group = models.ForeignKey(MemberGroup, null=True)

    def get_absolute_url(self):
        return reverse('edit-member', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class EventType(models.Model):
    name = models.TextField(null=False) 
    default_start_hour = models.IntegerField()
    default_end_hour = models.IntegerField()


class Event(models.Model):
    name = models.TextField()
    event_type = models.ForeignKey(EventType, null=True)
    start_dt = models.DateTimeField(null=False)
    end_dt = models.DateTimeField(null=False)
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

    def was_adequate(self):
        attendance_minutes = self.event.duration_minutes * self.attendance
        base_required_attendance_minutes = 60
        scaled_half_required_attendance_minutes = self.event.duration_minutes * 0.5

        return attendance_minutes > min(base_required_attendance_minutes, scaled_half_required_attendance_minutes)
