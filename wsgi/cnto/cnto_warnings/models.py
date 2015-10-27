import calendar

from django.db import models
from django.utils import timezone
from django.utils.timezone import datetime
from cnto.models import Event, Member, CreatedModifiedMixin, Attendance


class MemberWarningType(models.Model):
    name = models.TextField(null=False)


class MemberWarning(CreatedModifiedMixin):
    member = models.ForeignKey(Member, null=False)
    warning_type = models.ForeignKey(MemberWarningType, null=False)
    message = models.TextField(null=False)
    acknowledged = models.BooleanField(default=False)

