from django.utils import timezone
from django.db import models

# Create your models here.
from django.utils.html import escape
from cnto.models import Member


class Note(models.Model):
    member = models.ForeignKey(Member, null=False, related_name="notes")
    message = models.TextField(null=False)
    dt = models.DateTimeField(verbose_name="Note date", null=False, default=timezone.now)
    active = models.BooleanField(default=True)

    @staticmethod
    def get_active_note_message_for_member(member):
        note = Note.objects.all()[0].message
        return note

    def get_width_limited_message(self, width_limit=70):
        words = self.message.split(" ")
        rows = []
        current_row = ""
        for word in words:
            while len(word) > width_limit:
                if len(current_row) > 0:
                    rows.append(current_row)
                    current_row = ""

                rows.append(word[0:width_limit])
                word = word[width_limit:]

            current_row += word + " "
            if len(current_row) > width_limit:
                rows.append(current_row)
                current_row = ""

        if len(current_row) > 0:
            rows.append(current_row)

        final_message = " ".join(rows)

        return final_message

    def __str__(self):
        return self.message
