from django import  forms

class RegistrationForm(forms.Form):
    site_url = forms.URLField()
    email    = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)
    phone    = forms.CharField(required = False)

class ResendVerficationLink(forms.Form):
    email    = forms.EmailField()