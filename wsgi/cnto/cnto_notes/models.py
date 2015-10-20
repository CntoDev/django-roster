from django.utils import timezone
from django.db import models

# Create your models here.
from cnto.models import Member


class Note(models.Model):
    member = models.ForeignKey(Member, null=False)
    message = models.TextField(null=False)
    dt = models.DateTimeField(verbose_name="Note date", null=False, default=timezone.now)
    active = models.BooleanField(default=True)

