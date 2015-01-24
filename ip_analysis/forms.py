# -*- coding: utf-8 -*-

from django import forms

from utils.constants import ACCESS_STATUS, RULES_ACTION, ACCESS_STATUS_MAP, RULES_ACTION_1


class DateInput(forms.DateInput):
    input_type = 'date'


class IpAccessStatusForm(forms.Form):
    ip_address_add      =   forms.IPAddressField()
    access_status_add   =   forms.HiddenInput()

    def clean_access_status(self):
        if not self.cleaned_data['access_status'] in ACCESS_STATUS:
            raise forms.ValidationError("Invalid Access Status.")
        return ACCESS_STATUS_MAP[self.cleaned_data['access_status']]


class IpAccessStatusWithNoInputForm(forms.Form): # For IP Analysis Page
    ip_address      =   forms.HiddenInput()
    access_status   =   forms.HiddenInput()

    def clean_access_status(self):
        if not self.cleaned_data['access_status'] in ACCESS_STATUS:
            raise forms.ValidationError("Invalid Access Status.")
        return ACCESS_STATUS_MAP[self.cleaned_data['access_status']]


class IpAccessStatusDeleteForm(forms.Form):
    pass


class IpAccessStatusSearchForm(forms.Form):
    ip_address      =   forms.CharField(required = False)
    location        =   forms.CharField(required = False)
    isp             =   forms.CharField(required = False)
    organization    =   forms.CharField(required = False)
    access_status   =   forms.CharField(required = False)


class IpAnalysisSearchForm(forms.Form):
    ip_address      =   forms.CharField(required = False)
    country_name    =   forms.CharField(required = False)
    isp             =   forms.CharField(required = False)
    city_name       =   forms.CharField(required = False)
    status          =   forms.CharField(required = False)


class PagesPerMinuteRulesForm(forms.Form):
    action = forms.ChoiceField(choices=RULES_ACTION)


class PagesPerSessionRulesForm(forms.Form):
    pages_per_session = forms.IntegerField(initial=100)
    action = forms.ChoiceField(choices=RULES_ACTION)


class SessionLengthRulesForm(forms.Form):
    session_length = forms.IntegerField(initial=100)
    action = forms.ChoiceField(choices=RULES_ACTION)


class BrowserIntegrityCheckForm(forms.Form):
    action = forms.ChoiceField(choices=RULES_ACTION)


class HTTPRequestIntegrityCheckForm(forms.Form):
    action = forms.ChoiceField(choices=RULES_ACTION)


class AggregatorCheckForm(forms.Form):
    action = forms.ChoiceField(choices=RULES_ACTION)


class BehaviourIntegrityCheckForm(forms.Form):
    action = forms.ChoiceField(choices=RULES_ACTION)


class SessionLengthcheckForm(forms.Form):
    action = forms.ChoiceField(choices=RULES_ACTION)


class IpActionForm(forms.Form):
    action              =   forms.ChoiceField(choices=RULES_ACTION_1)
    expiry_date         =   forms.DateField(widget = forms.DateInput())


class IpActionUpdateForm(forms.Form):
    ip_address          =   forms.IPAddressField()
    action              =   forms.ChoiceField(choices=RULES_ACTION_1)
    expiry_date         =   forms.DateField(widget = forms.DateInput())

