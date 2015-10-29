# -*- coding: utf-8 -*-
from django.utils import timezone
from django import forms

from bootstrap3_datetime.widgets import DateTimePicker
from models import Member, MemberGroup, Rank, EventType, Absence, AbsenceType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, BaseInput
from crispy_forms.bootstrap import FormActions
from utils.date_utils import dates_overlap


class AcceptButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn btn-primary'


class CancelButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn btn-default'


class EventTypeForm(forms.models.ModelForm):
    class Meta:
        model = EventType
        fields = ['name', 'default_start_hour', 'default_end_hour', 'minimum_required_attendance_minutes',
                  'css_class_name']

    def __init__(self, *args, **kwargs):
        super(EventTypeForm, self).__init__(*args, **kwargs)
        self.fields['css_class_name'].required = False

    name = forms.CharField()
    default_start_hour = forms.IntegerField()
    default_end_hour = forms.IntegerField()
    minimum_required_attendance_minutes = forms.IntegerField()
    css_class_name = forms.CharField(help_text="Class name may be left blank and is used for calendar styling.")

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name'),
        Field('default_start_hour'),
        Field('default_end_hour'),
        Field('minimum_required_attendance_minutes'),
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
        fields = ['name', 'member_group', 'rank', 'join_date', 'mods_assessed', 'discharged', 'discharge_date', 'email']

    name = forms.CharField()
    member_group = forms.ModelChoiceField(queryset=MemberGroup.objects.all(),
                                          empty_label="<Select group>")
    rank = forms.ModelChoiceField(queryset=Rank.objects.all(), empty_label=None)
    join_date = forms.DateField(initial=timezone.now(), label="Join date", widget=DateTimePicker(options={
        "format": "YYYY-MM-DD",
        "pickTime": False
    }))

    email = forms.EmailField(required=False)

    mods_assessed = forms.BooleanField(required=False)
    discharged = forms.BooleanField(required=False)

    discharge_date = forms.DateField(label="Discharge date", widget=DateTimePicker(options={
        "format": "YYYY-MM-DD",
        "pickTime": False
    }),
                                     required=False)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name'),
        Field('member_group'),
        Field('rank'),
        Field('join_date'),
        Field('email'),
        Field('mods_assessed'),
        Field('discharged'),
        Field('discharge_date', type='hidden'),
        FormActions(
            AcceptButton('save_changes', 'Save changes'),
            CancelButton('cancel', 'Cancel'),
        )
    )

    def clean_discharged(self):
        discharged = self.cleaned_data['discharged']
        name = self.cleaned_data['name']

        undischarged_members_with_name = Member.objects.filter(name=name, discharged=False, deleted=False)
        if not discharged and len(undischarged_members_with_name) > 0 and \
                undischarged_members_with_name[0] != self.instance:
            raise forms.ValidationError(
                "Undischarged member with this name already exists.  Choose another name or discharge the other "
                "member.")

        return discharged


class DischargedMemberForm(forms.models.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'join_date', 'discharged', 'discharge_date']

    name = forms.CharField()
    join_date = forms.DateField(label="Join date", widget=DateTimePicker(options={
        "format": "YYYY-MM-DD",
        "pickTime": False
    }))
    discharged = forms.BooleanField(required=False)
    discharge_date = forms.DateField(label="Discharge date", widget=DateTimePicker(options={
        "format": "YYYY-MM-DD",
        "pickTime": False
    }),
                                     required=False)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name'),
        Field('join_date'),
        Field('discharged'),
        Field('discharge_date'),
        FormActions(
            AcceptButton('save_changes', 'Save changes'),
            CancelButton('cancel', 'Cancel'),
        )
    )

    def clean_discharged(self):
        discharged = self.cleaned_data['discharged']
        name = self.cleaned_data['name']
        undischarged_members_with_name = Member.objects.filter(name=name, discharged=False, deleted=False)
        if not discharged and len(undischarged_members_with_name) > 0 and \
                undischarged_members_with_name[0] != self.instance:
            raise forms.ValidationError(
                "Undischarged member with this name already exists.  Choose another name or discharge the other "
                "member.")

        return discharged


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
        fields = ['absence_type', 'start_date', 'end_date', 'member', 'concluded']

    absence_type = forms.ModelChoiceField(queryset=AbsenceType.objects.all())

    start_date = forms.DateField(label="Start date", widget=DateTimePicker(options={
        "format": "YYYY-MM-DD",
        "pickTime": False
    }))

    end_date = forms.DateField(label="End date", widget=DateTimePicker(options={
        "format": "YYYY-MM-DD",
        "pickTime": False
    }))

    concluded = forms.BooleanField(required=False)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('absence_type'),
        Field('start_date'),
        Field('end_date'),
        Field('concluded'),
        Field('member', type="hidden"),
        FormActions(
            AcceptButton('save_changes', 'Save changes', css_class="btn-primary"),
            CancelButton('cancel', 'Cancel', css_class="btn-default"),
        )
    )

    def clean_end_date(self):
        member_pk = self.data['member']
        member = Member.objects.get(pk=member_pk)
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        if end_date <= start_date:
            raise forms.ValidationError("Absence end date on or before start date!")

        for absence in Absence.objects.filter(member=member, deleted=False):
            if dates_overlap(start_date, end_date, absence.start_date, absence.end_date) and absence != self.instance:
                raise forms.ValidationError(
                    "Absence overlaps with another absence from %s to %s!" % (absence.start_date, absence.end_date))

        return end_date
