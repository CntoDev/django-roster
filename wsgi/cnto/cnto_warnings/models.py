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
        if recipient.email is not None and len(recipient.email) > 0:
            recipient_emails.append(recipient.email)

    if len(recipient_emails) == 0:
        return None
    else:
        return ";".join(recipient_emails)


class MemberWarningType(models.Model):
    """

    """
    name = models.TextField(null=False)

    def is_warning(self, warning_name):
        if warning_name.lower() in self.name.lower():
            return True
        else:
            return False


class MemberWarning(CreatedModifiedMixin):
    """

    """
    member = models.ForeignKey(Member, null=False)
    warning_type = models.ForeignKey(MemberWarningType, null=False)
    message = models.TextField(null=False)
    acknowledged = models.BooleanField(default=False)
    notified = models.BooleanField(default=False, null=False)

    def get_recipients_string(self):
        """

        :return:
        """
        recipient_users = []
        if self.warning_type.is_warning("Mod Assessment Due") or self.warning_type.is_warning(
                "Grunt Qualification Due"):
            recipient_users = [
                User.objects.get(username__iexact="admin"),
                User.objects.get(username__iexact="abuk"),
                User.objects.get(username__iexact="john"),
            ]
        elif self.warning_type.is_warning("Contribution Expiring"):
            recipient_users = [
                User.objects.get(username__iexact="admin"),
                User.objects.get(username__iexact="clarke"),
                User.objects.get(username__iexact="ryujin"),
            ]
        elif self.warning_type.is_warning("Low Attendance"):
            recipient_users = [
                User.objects.get(username__iexact="admin"),
            ]

            if self.member.member_group.leader is not None:
                recipient_users.append(self.member.member_group.leader)

        if len(recipient_users) > 0:
            return recipients_to_recipient_string(recipient_users)
        else:
            return None

    def get_subject_and_body(self):
        """

        :return:
        """
        subject = None
        body = None

        if self.warning_type.is_warning("Mod Assessment Due"):
            subject = "Mod assessment for %s overdue" % (self.member.name,)
            body = "%s didn't report to have his mods assessed within two weeks of joining our community." % (
                self.member.name,)
        elif self.warning_type.is_warning("Grunt Qualification Due"):
            subject = "Grunt Qualification for %s overdue" % (self.member.name,)
            body = "%s didn't qualify to become a Grunt within 6 weeks of joining our community." % (self.member.name,)
        elif self.warning_type.is_warning("Contribution Expiring"):
            subject = "Contribution for %s expiring" % (self.member.name,)
            body = "%s" % (self.message,)
        elif self.warning_type.is_warning("Low Attendance"):
            subject = "Low Attendance for %s" % (self.member.name,)
            body = "%s" % (self.message,)

        return subject, body
