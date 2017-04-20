# -*- coding: utf-8 -*-
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, BaseInput
from crispy_forms.bootstrap import FormActions

from .models import Member, MemberGroup, Rank, EventType, Absence, AbsenceType
from utils.date_utils import dates_overlap


class AcceptButton(BaseInput):
    """None

    """
    input_type = 'submit'
    field_classes = 'btn btn-primary'


class CancelButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn btn-default'


class EventTypeForm(forms.models.ModelForm):
    class Meta:
        model = EventType
        fields = ['name', 'default_start_hour', 'default_end_hour', 'minimum_required_attendance_ratio',
                  'css_class_name']

    def __init__(self, *args, **kwargs):
        super(EventTypeForm, self).__init__(*args, **kwargs)
        self.fields['css_class_name'].required = False

    name = forms.CharField()
    default_start_hour = forms.IntegerField()
    default_end_hour = forms.IntegerField()
    minimum_required_attendance_ratio = forms.FloatField(
        help_text="Ratio should be between 0.0 and 1.0, where 1.0 = 100% of event duration attended.  The configured "
                  "Coop ratio will be used for Friday attendance.  Monday and Wednesday Coop events require double the "
                  "attendance of Friday Coop events.")
    css_class_name = forms.CharField(help_text="Class name may be left blank and is used for calendar styling.")

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name'),
        Field('default_start_hour'),
        Field('default_end_hour'),
        Field('minimum_required_attendance_ratio'),
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


class MergeMemberIntoForm(forms.Form):
    """None

    """

    from_member = forms.ModelChoiceField(queryset=Member.objects.all().order_by('name'),
                                         empty_label="<Select member>", required=True)

    into_member = forms.ModelChoiceField(queryset=Member.active_members().order_by('name'),
                                         empty_label="<Select member>", required=True,
                                         help_text="This is the member that will remain after merge. The 'from' "
                                                   "member will be deleted, "
                                                   "but all of the information associated with that member will be "
                                                   "merged into this member.")

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('from_member'),
        Field('into_member'),
        FormActions(
            AcceptButton('save_changes', 'Merge'),
            CancelButton('cancel', 'Cancel'),
        )
    )

    def clean_into_member(self):
        from_member = self.cleaned_data['from_member']
        into_member = self.cleaned_data['into_member']

        if from_member == into_member:
            raise forms.ValidationError(
                "Cannot merge member into itself!")

        return into_member


class MemberForm(forms.models.ModelForm):
    """None

    """

    class Meta:
        model = Member
        fields = ['name', 'member_group', 'rank', 'join_date', 'mods_assessed', 'bqf_assessed', 'discharged',
                  'discharge_date', 'email', 'bi_name']

    name = forms.CharField()
    member_group = forms.ModelChoiceField(queryset=MemberGroup.objects.all(),
                                          empty_label="<Select group>")
    rank = forms.ModelChoiceField(queryset=Rank.objects.all(), empty_label=None)
    join_date = forms.DateField(label="Join date", widget=DateTimePicker(options={
        "format": "YYYY-MM-DD",
        "pickTime": False
    }))

    email = forms.EmailField(required=False)
    bi_name = forms.CharField(required=False, label="BI nickname")

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
        Field('bi_name'),
        Field('mods_assessed'),
        Field('bqf_assessed'),
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
        fields = ['name', 'leader']

    name = forms.CharField()
    leader = forms.ModelChoiceField(
        queryset=Member.qualified_leaders().order_by("name"),
        required=False)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name'),
        Field('leader'),
        FormActions(
            AcceptButton('save_changes', 'Save changes', css_class="btn-primary"),
            CancelButton('cancel', 'Cancel', css_class="btn-default"),
        )
    )

    def clean_leader(self):
        leader = self.cleaned_data['leader']
        if leader is None:
            return None

        if leader.email is None or "@" not in leader.email:
            raise forms.ValidationError(
                "Cannot select a leader with no configured email address!")

        return leader


class AbsenceForm(forms.models.ModelForm):
    class Meta:
        model = Absence
        fields = ['absence_type', 'start_date', 'end_date', 'member', 'concluded']

    absence_type = forms.ModelChoiceField(queryset=AbsenceType.objects.all().filter(deprecated=False))

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
