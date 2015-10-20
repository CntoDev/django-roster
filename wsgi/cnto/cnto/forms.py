# -*- coding: utf-8 -*-
from django import forms

from bootstrap3_datetime.widgets import DateTimePicker
from models import Member, MemberGroup, Rank, EventType, Absence, AbsenceType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, BaseInput
from crispy_forms.bootstrap import FormActions


class AcceptButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn btn-primary'


class CancelButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn btn-default'


class EventTypeForm(forms.models.ModelForm):
    class Meta:
        model = EventType
        fields = ['name', 'default_start_hour', 'default_end_hour', 'css_class_name']

    def __init__(self, *args, **kwargs):
        super(EventTypeForm, self).__init__(*args, **kwargs)
        self.fields['css_class_name'].required = False

    name = forms.CharField()
    default_start_hour = forms.IntegerField()
    default_end_hour = forms.IntegerField()
    css_class_name = forms.CharField(help_text="Class name may be left blank and is used for calendar styling.")

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name'),
        Field('default_start_hour'),
        Field('default_end_hour'),
        Field('css_class_name'),
        FormActions(
            AcceptButton('save_changes', 'Save changes', css_class="btn-primary"),
            CancelButton('cancel', 'Cancel', css_class="btn-default"),
        )
    )

    def clean_css_class_name(self):
        name = self.cleaned_data['css_class_name']
        if name is None:
            name = ""
        return name


class MemberForm(forms.models.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'member_group', 'rank', 'join_dt', 'mods_assessed', 'discharged', 'discharge_dt']

    name = forms.CharField()
    member_group = forms.ModelChoiceField(queryset=MemberGroup.objects.all(),
                                          empty_label="<Select group>")
    rank = forms.ModelChoiceField(queryset=Rank.objects.all(),
                                  empty_label="<Select rank>")
    join_dt = forms.DateField(label="Join date", widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                "pickTime": False}))
    mods_assessed = forms.BooleanField(required=False)
    discharged = forms.BooleanField(required=False)

    discharge_dt = forms.DateField(label="Discharge date", widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                          "pickTime": False}),
                                   required=False)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name'),
        Field('member_group'),
        Field('rank'),
        Field('join_dt'),
        Field('mods_assessed'),
        Field('discharged'),
        Field('discharge_dt', type='hidden'),
        FormActions(
            AcceptButton('save_changes', 'Save changes'),
            CancelButton('cancel', 'Cancel'),
        )
    )


class DischargedMemberForm(forms.models.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'join_dt', 'discharged', 'discharge_dt']

    name = forms.CharField()
    join_dt = forms.DateField(label="Join date", widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                "pickTime": False}))
    discharged = forms.BooleanField(required=False)
    discharge_dt = forms.DateField(label="Discharge date", widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                          "pickTime": False}),
                                   required=False)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name'),
        Field('join_dt'),
        Field('discharged'),
        Field('discharge_dt'),
        FormActions(
            AcceptButton('save_changes', 'Save changes'),
            CancelButton('cancel', 'Cancel'),
        )
    )


class MemberGroupForm(forms.models.ModelForm):
    class Meta:
        model = MemberGroup
        fields = ['name']

    name = forms.CharField()

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name'),
        FormActions(
            AcceptButton('save_changes', 'Save changes', css_class="btn-primary"),
            CancelButton('cancel', 'Cancel', css_class="btn-default"),
        )
    )


class AbsenceForm(forms.models.ModelForm):
    class Meta:
        model = Absence
        fields = ['absence_type', 'start_dt', 'end_dt', 'member']

    absence_type = forms.ModelChoiceField(queryset=AbsenceType.objects.all())

    start_dt = forms.DateField(label="Start date", widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                  "pickTime": False}))

    end_dt = forms.DateField(label="End date", widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                              "pickTime": False}))

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('absence_type'),
        Field('start_dt'),
        Field('end_dt'),
        Field('member', type="hidden"),
        FormActions(
            AcceptButton('save_changes', 'Save changes', css_class="btn-primary"),
            CancelButton('cancel', 'Cancel', css_class="btn-default"),
        )
    )
