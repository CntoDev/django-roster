from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.timezone import timedelta
from django.db.models import Q

from cnto import RECRUIT_RANK


class CreatedModifiedMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(null=False, default=timezone.now)
    modified = models.DateTimeField(null=False, default=timezone.now)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.created = timezone.now()

        self.modified = timezone.now()

        super(CreatedModifiedMixin, self).save(*args, **kwargs)


class Rank(models.Model):
    name = models.TextField(null=False, unique=True)

    def __str__(self):
        return self.name

    def lowered_name(self):
        return self.name.lower()


class MemberGroup(models.Model):
    name = models.TextField(null=False, unique=True)
    leader = models.ForeignKey('Member', null=True, default=None)

    def __str__(self):
        return self.name

    def lowered_name(self):
        return self.name.lower()

    def member_count(self):
        return Member.objects.all().filter(member_group=self).count()


class Member(models.Model):
    class Meta:
        permissions = (
            ("cnto_edit_members", u"Edit members"),
            ("cnto_view_absentees", u"View absentees"),
            ("cnto_view_reports", u"View reports"),
            ("cnto_edit_groups", u"Edit groups"),
            ("cnto_edit_event_types", u"Edit event types"),
            ("cnto_view_events", u"View events"),
            ("cnto_edit_events", u"Edit events"),
        )

    name = models.TextField(null=False, unique=False)
    rank = models.ForeignKey(Rank, null=False)
    member_group = models.ForeignKey(MemberGroup, null=True)
    email = models.EmailField(null=True)

    join_date = models.DateField(verbose_name="Join date", null=False, default=timezone.now)

    discharged = models.BooleanField(default=False, null=False)
    discharge_date = models.DateField(verbose_name="Discharge date", null=True, default=None)

    mods_assessed = models.BooleanField(default=True, null=False)
    deleted = models.BooleanField(default=False, null=False)

    @staticmethod
    def qualified_leaders():
        rank_list = ['ssgt', 'spc']
        results = Member.objects.none()
        for name in rank_list:
            results |= Member.objects.filter(rank__name__iexact=name, deleted=False, discharged=False)

        return results

    @staticmethod
    def active_members(include_recruits=True):
        members = Member.objects.all().filter(deleted=False, discharged=False)

        if not include_recruits:
            recruit_rank = Rank.objects.get(name__iexact=RECRUIT_RANK)
            members = members.filter(~Q(rank=recruit_rank))

        return members

    @staticmethod
    def recruits():
        return Member.active_members(include_recruits=True).filter(rank__name__iexact=RECRUIT_RANK)

    @staticmethod
    def active_members_after_dt(dt):
        members = Member.active_members()
        members = members.filter(join_date__lte=dt.date())

        return members

    def gqf_due_days(self):
        if RECRUIT_RANK not in self.rank.name.lower():
            return "-"
        else:
            return (self.get_gqf_deadline_date() - timezone.now().date()).days

    def mod_due_days(self):
        if RECRUIT_RANK not in self.rank.name.lower() or self.mods_assessed:
            return "-"
        else:
            return (self.get_mod_assessment_deadline_date() - timezone.now().date()).days

    def is_absent(self):
        current_dt = timezone.now()
        absences = Absence.objects.filter(deleted=False, concluded=False, member=self,
                                          start_date__lte=current_dt.date(),
                                          end_date__gte=current_dt.date())

        return absences.count() > 0

    def is_recruit(self):
        return RECRUIT_RANK in self.rank.name.lower()

    def get_total_days_absent(self):
        absences = Absence.objects.filter(member=self)
        total_absent_duration_days = 0
        for absence in absences:
            total_absent_duration_days += (absence.end_date - absence.start_date).days

        return total_absent_duration_days

    def get_recruit_event_attendance_deadline_and_count(self):
        absent_days = self.get_total_days_absent()
        return self.join_date + timedelta(days=60) + timedelta(days=absent_days), 5

    def get_gqf_deadline_date(self):
        absent_days = self.get_total_days_absent()
        return self.join_date + timedelta(days=42) + timedelta(days=absent_days)

    def get_mod_assessment_deadline_date(self):
        absent_days = self.get_total_days_absent()
        return self.join_date + timedelta(days=14) + timedelta(days=absent_days)

    def get_absolute_url(self):
        return reverse('edit-member', kwargs={'pk': self.pk})

    def is_mod_assessment_due(self):
        """

        :return:
        """
        current_dt = timezone.now()

        mod_assessment_deadline = self.get_mod_assessment_deadline_date()
        if current_dt.date() > mod_assessment_deadline and not self.mods_assessed:
            # Two weeks mod assessment
            message = "Mod assessment overdue."
            return True, message

        return False, None

    def is_grunt_qualification_due(self):
        """

        :return:
        """
        current_dt = timezone.now()

        grunt_qualification_deadline = self.get_gqf_deadline_date()
        if current_dt.date() > grunt_qualification_deadline:
            # Six weeks grunt notice
            message = "Grunt qualification overdue."
            return True, message

        return False, None

    def get_recruit_warning(self):
        if RECRUIT_RANK not in self.rank.name.lower():
            return False, "Not recruit."

        mod_assessment_due, reason = self.is_mod_assessment_due()

        if mod_assessment_due:
            return True, reason

        grunt_qualification_due, reason = self.is_grunt_qualification_due()

        if grunt_qualification_due:
            return True, reason

        return False, "No warnings."

    def __str__(self):
        return self.name

    def lowered_name(self):
        return self.name.lower()


class EventType(models.Model):
    name = models.TextField(null=False)
    default_start_hour = models.IntegerField()
    default_end_hour = models.IntegerField()
    minimum_required_attendance_ratio = models.FloatField(null=False)
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
    deprecated = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name


class Absence(models.Model):
    member = models.ForeignKey(Member, null=False)
    absence_type = models.ForeignKey(AbsenceType, null=False)

    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    concluded = models.BooleanField(default=False, null=False)
    deleted = models.BooleanField(default=False, null=False)

    @staticmethod
    def get_absence_for_event(event, member):
        absence = Absence.objects.get(member=member, start_date__lte=event.start_dt.date(),
                                      end_date__gte=event.start_dt.date(), deleted=False)
        return absence

    def due_days(self):
        return (self.end_date - timezone.now().date()).days

    def __str__(self):
        return "%s for %s: %s to %s" % (self.absence_type.name, self.member.name, self.start_date, self.end_date)


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

        return {
            "duration_minutes": event.duration_minutes, "average_attendance": average_attendance,
            "player_count": len(attendances)
        }

    event = models.ForeignKey(Event, null=False)
    member = models.ForeignKey(Member, null=False)
    attendance = models.FloatField(null=False)

    class Meta:
        unique_together = ('event', 'member',)

    @staticmethod
    def was_adequate_for_period(member, events, start_dt, end_dt, min_total_events=1, adequate_if_absent=False):
        if member.join_date > start_dt.date():
            return True, "Was not a member for entire period."

        if adequate_if_absent:
            start_absences_for_period = Absence.objects.filter(member=member, start_date__lte=start_dt.date(),
                                                               end_date__gte=start_dt.date())
            end_absences_for_period = Absence.objects.filter(member=member, start_date__lte=end_dt.date(),
                                                             end_date__gte=end_dt.date())
            inside_absences_for_period = Absence.objects.filter(member=member, start_date__gte=start_dt.date(),
                                                                end_date__lte=end_dt.date())
            overlap_absences_for_period = Absence.objects.filter(member=member, start_date__lte=start_dt.date(),
                                                                 end_date__gte=end_dt.date())

            absent_days = (
                start_absences_for_period.count() + end_absences_for_period.count() +
                inside_absences_for_period.count() + overlap_absences_for_period.count())

            if absent_days > 0:
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

        min_trainings = 0

        between_string = "between %s and %s" % (start_dt.strftime("%Y-%m-%d"), end_dt.strftime("%Y-%m-%d"))

        if attended_total < min_total_events:
            return False, "Did not attend enough events %s." % (between_string,)
        if attended_training < min_trainings:
            return False, "Did not attend enough trainings %s." % (between_string,)

        return True, "No attendance issues."

    def was_adequate(self):
        """

        :return:
        """
        attendance_ratio = self.attendance
        base_required_attendance_ratio = self.event.event_type.minimum_required_attendance_ratio

        # event_dow = self.event.start_dt.weekday()
        # if self.event.event_type == EventType.objects.get(name__iexact="coop") and event_dow in [0, 2]:
        #     # Coop on Mondays and Wednesdays require double the attendance of normal Coops.
        #     base_required_attendance_ratio *= 2

        return attendance_ratio > base_required_attendance_ratio
