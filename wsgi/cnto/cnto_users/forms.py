# -*- coding: utf-8 -*-
from django import forms

from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, BaseInput
from crispy_forms.bootstrap import FormActions


class AcceptButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn btn-primary'


class CancelButton(BaseInput):
    input_type = 'submit'
    field_classes = 'btn btn-default'


class EditPasswordForm(forms.Form):
    username = forms.CharField()
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('username', type="hidden"),
        Field('current_password'),
        Field('new_password'),
        Field('confirm_password'),
        FormActions(
            AcceptButton('save_changes', 'Save changes', css_class="btn-primary"),
            CancelButton('cancel', 'Cancel', css_class="btn-default"),
        )
    )

    def clean_current_password(self):
        username = self.cleaned_data["username"]
        current_password = self.cleaned_data["current_password"]
        user = authenticate(username=username, password=current_password)
        if user is None:
            raise forms.ValidationError("Invalid password!")

        return current_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data["new_password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return confirm_password
