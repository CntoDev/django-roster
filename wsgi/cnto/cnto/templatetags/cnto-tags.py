from django import template
from cnto_notes.models import Note

register = template.Library()


def value_of(value, arg):
    func = getattr(value, arg)
    return func()


def active_note_message(member):
    try:
        member_note = Note.objects.get(member=member, active=True)
        note_message = member_note.message
        message_length_limit = 60
        if len(note_message) > message_length_limit:
            return note_message[0:message_length_limit - 3] + "..."
        else:
            return note_message
    except Note.DoesNotExist:
        return ""


register.filter('value_of', value_of)
register.filter('active_note_message', active_note_message)