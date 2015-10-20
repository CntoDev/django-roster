# -*- coding: utf-8 -*-
from django import forms

from cnto.forms import AcceptButton, CancelButton
from cnto_notes.models import Note
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import FormActions


class NoteForm(forms.models.ModelForm):
    class Meta:
        model = Note
        fields = ['message']

    message = forms.CharField()

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('message'),
        FormActions(
            AcceptButton('save_changes', 'Save changes', css_class="btn-primary"),
            CancelButton('cancel', 'Cancel', css_class="btn-default"),
        )
    )
