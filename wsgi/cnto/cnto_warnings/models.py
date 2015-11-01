from django.db import models
from cnto.models import Member, CreatedModifiedMixin


class MemberWarningType(models.Model):
    name = models.TextField(null=False)


class MemberWarning(CreatedModifiedMixin):
    member = models.ForeignKey(Member, null=False)
    warning_type = models.ForeignKey(MemberWarningType, null=False)
    message = models.TextField(null=False)
    acknowledged = models.BooleanField(default=False)
    notified = models.BooleanField(default=False, null=False)
