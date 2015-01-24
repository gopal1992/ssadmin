from django import forms

class AggregatorAnalysisSearchForm(forms.Form):
    ip_address      =   forms.CharField(required = False)
    country_name    =   forms.CharField(required = False)
    isp             =   forms.CharField(required = False)
    city_name       =   forms.CharField(required = False)
    aggregator_name =   forms.CharField(required = False)