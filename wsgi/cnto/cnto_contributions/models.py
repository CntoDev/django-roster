from django.db import models
from cnto.models import Member


class ContributionType(models.Model):
    name = models.TextField(null=False)

    def __str__(self):
        return self.name


class Contribution(models.Model):
    class Meta:
        permissions = (
            ("cnto_edit_contributions", u"Edit contributions"),
        )

    member = models.ForeignKey(Member, null=False)
    type = models.ForeignKey(ContributionType, null=False)

    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
