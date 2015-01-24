from django import forms


class UserAnalysisSearchForm(forms.Form):
    user_id =   forms.CharField(required = False)
