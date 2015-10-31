# -*- coding: utf-8 -*-
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms

from cnto.forms import AcceptButton, CancelButton
from cnto_contributions.models import Contribution, ContributionType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import FormActions


class ContributionForm(forms.models.ModelForm):
    class Meta:
        model = Contribution
        fields = ['type', 'start_date', 'end_date', 'member']

    type = forms.ModelChoiceField(queryset=ContributionType.objects.all())
    start_date = forms.DateField(label="Start date", widget=DateTimePicker(options={
        "format": "YYYY-MM-DD",
        "pickTime": False
    }))
    end_date = forms.DateField(label="End date", widget=DateTimePicker(options={
        "format": "YYYY-MM-DD",
        "pickTime": False
    }))

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('type'),
        Field('start_date'),
        Field('end_date'),
        Field('member', type="hidden"),
        FormActions(
            AcceptButton('save_changes', 'Save changes', css_class="btn-primary"),
            CancelButton('cancel', 'Cancel', css_class="btn-default"),
        )
    )
