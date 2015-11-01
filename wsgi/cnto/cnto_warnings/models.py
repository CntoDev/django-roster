from django.contrib.auth.models import User
from django.db import models
from cnto.models import Member, CreatedModifiedMixin


def recipients_to_recipient_string(recipient_users):
    """

    :param recipient_users:
    :return:
    """
    recipient_emails = []
    for recipient in recipient_users:
        if len(recipient.email) > 0:
            recipient_emails.append(recipient.email)

    if len(recipient_emails) == 0:
        return None
    else:
        return ";".join(recipient_emails)


class MemberWarningType(models.Model):
    name = models.TextField(null=False)


class MemberWarning(CreatedModifiedMixin):
    member = models.ForeignKey(Member, null=False)
    warning_type = models.ForeignKey(MemberWarningType, null=False)
    message = models.TextField(null=False)
    acknowledged = models.BooleanField(default=False)
    notified = models.BooleanField(default=False, null=False)

    def get_recipients_string(self):
        """

        :return:
        """
        mod_warning_type = MemberWarningType.objects.get(name__iexact="Mod Assessment Due")
        grunt_warning_type = MemberWarningType.objects.get(name__iexact="Grunt Qualification Due")
        contribution_expiring_type = MemberWarningType.objects.get(name__iexact="Contribution Expiring")

        recipient_users = []
        if self.warning_type in [mod_warning_type, grunt_warning_type]:
            recipient_users = [
                User.objects.get(username__iexact="admin"),
                User.objects.get(username__iexact="abuk"),
                User.objects.get(username__iexact="john"),
            ]
        elif self.warning_type == contribution_expiring_type:
            recipient_users = [
                User.objects.get(username__iexact="admin"),
                User.objects.get(username__iexact="clarke"),
                User.objects.get(username__iexact="ryujin"),
            ]

        if len(recipient_users) > 0:
            return recipients_to_recipient_string(recipient_users)
        else:
            return None

    def get_subject_and_body(self):
        """

        :return:
        """
        mod_warning_type = MemberWarningType.objects.get(name__iexact="Mod Assessment Due")
        grunt_warning_type = MemberWarningType.objects.get(name__iexact="Grunt Qualification Due")
        contribution_expiring_type = MemberWarningType.objects.get(name__iexact="Contribution Expiring")

        subject = None
        body = None

        if self.warning_type == mod_warning_type:
            subject = "Mod assessment for %s overdue" % (self.member.name,)
            body = "%s didn't report to have his mods assessed within two weeks of joining our community." % (
                self.member.name,)
        elif self.warning_type == grunt_warning_type:
            subject = "Grunt Qualification for %s overdue" % (self.member.name,)
            body = "%s didn't qualify to become a Grunt within 6 weeks of joining our community." % (self.member.name,)
        elif self.warning_type == contribution_expiring_type:
            subject = "Contribution for %s expiring" % (self.member.name,)
            body = "%s" % (self.message,)

        return subject, body
