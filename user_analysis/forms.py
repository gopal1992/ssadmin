# -*- coding: utf-8 -*-

from django import forms

from utils.constants import ACCESS_STATUS, ACCESS_STATUS_MAP


class UserAccessStatusForm(forms.Form):
    user_id_add     =   forms.CharField()
    access_status   =   forms.HiddenInput()# Hard code the value
    access_type     =   forms.HiddenInput()

    def clean_access_status(self):
        if not self.cleaned_data['access_status'] in ACCESS_STATUS:
            raise forms.ValidationError("Invalid Access Status.")
        return ACCESS_STATUS_MAP[self.cleaned_data['access_status']]


class UserAccessStatusSearchForm(forms.Form):
    user_id         =  forms.CharField(required = False)


class UserAccessStatusDeleteForm(forms.Form):
    pass
