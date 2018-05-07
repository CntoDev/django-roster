from django import template
from django.contrib.auth.models import Group, Permission
from django.utils import timezone
from cnto_contributions.models import Contribution
from cnto_notes.models import Note

register = template.Library()


@register.filter(name='value_of')
def value_of(value, arg):
    func = getattr(value, arg)
    return func()


@register.filter(name='active_note_message')
def active_note_message(member):
    try:
        member_note = member.notes.get(active=True)
        note_message = member_note.message
        message_length_limit = 70
        if len(note_message) > message_length_limit:
            return note_message[0:message_length_limit - 3] + "..."
        else:
            return note_message
    except Note.DoesNotExist:
        return ""


@register.filter(name='contribution_level')
def contribution_level(member):
    contributions = Contribution.objects.filter(member=member, end_date__gte=timezone.now().date())

    if contributions.count() == 0:
        return ""
    else:
        return contributions[0].type.name


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name__iexact=group_name).exists()


@register.filter(name='has_permission')
def has_permission(user, permission_name):
    if user.is_superuser:
        return True

    for group in user.groups.all():
        if group.permissions.all().filter(codename=permission_name).exists():
            return True

    return False
