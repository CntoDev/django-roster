# -*- coding: utf-8 -*-
from django import forms

from models import Member, MemberGroup, Rank, EventType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions


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
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
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
        fields = ['name', 'member_group', 'rank']

    name = forms.CharField()
    member_group = forms.ModelChoiceField(queryset=MemberGroup.objects.all(),
                                          empty_label="<Select group>")
    rank = forms.ModelChoiceField(queryset=Rank.objects.all(),
                                  empty_label="<Select rank>")

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name'),
        Field('member_group'),
        Field('rank'),
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
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
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )
