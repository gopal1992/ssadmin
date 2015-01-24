# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from accounts.forms import TIMEZONES, USER_PRIVILEGES
from ip_analysis.models import Subscriber, ResponseCode


SUBSCRIBER_MODE = [(1, "Monitor"), (2, "Active")]


def get_users():
    return User.objects.filter(is_active=True).values_list('username').\
        order_by('username')


def get_report_choices():
    # Note: Don't try to reverse. choices are evaluated before urls patterns
    # are loaded
    return [('/', 'Traffic Analysis'),
            ('/ip_analysis/', 'Bot IP Analysis'),
            ('/user_analysis/', 'User Analysis'),
            ('/aggregator/aggregator_analysis/', 'Aggregator Analysis'),
            ('/configuration/bot/', 'Bot Reponse List'),
            ('/ip_access_list/', 'IP Access List'),
            ('/user_access_list/', 'User Access List'),
            ('/getting_started/', 'Getting Started'),
            ('/subscriber_details/', 'Subscriber ID Details'),
            ('/download_connectors/', 'Download Connectors'),
            ('/verify_integration/', 'Verify Integration'),
            ]

class NewSubscriberForm(forms.Form):
    name            =   forms.CharField(max_length=256)
    site_url        =   forms.URLField(max_length=250)
    email           =   forms.EmailField(max_length=500)
    timezone        =   forms.ChoiceField(choices=TIMEZONES, initial="Asia/Kolkata")
    status          =   forms.IntegerField(initial = 1)
    phone1          =   forms.CharField(max_length = 75)
    phone2          =   forms.CharField(max_length = 75, required=False)
    address1        =   forms.CharField(widget = forms.Textarea, max_length = 500)
    address2        =   forms.CharField(widget = forms.Textarea, max_length = 500,required = False)
    mode            =   forms.ChoiceField(choices=SUBSCRIBER_MODE, initial="Active")

    r_browserIntgrity       = forms.ModelChoiceField(ResponseCode.objects.filter(id__in = (0, 2, )), initial={'reponse': 'Captcha'})
    r_httpRequestIntegrity  = forms.ModelChoiceField(ResponseCode.objects.filter(id__in = (0, 2, )), initial={'reponse': 'Captcha'})
    r_Aggregator            = forms.ModelChoiceField(ResponseCode.objects.filter(id__in = (0, 2, )), initial={'reponse': 'Allow'})
    r_behaviourIntegrity    = forms.ModelChoiceField(ResponseCode.objects.filter(id__in = (0, 2, )), initial={'reponse': 'Captcha'})
    r_Pagepermin            = forms.ModelChoiceField(ResponseCode.objects.filter(id__in = (0, 2, )), initial={'reponse': 'Captcha'})

    # Page permissions
    ip_analysis_page    = forms.BooleanField(initial= True, required=False)
    ip_access_page      = forms.BooleanField(initial= True, required=False)
    user_access_page    = forms.BooleanField(initial= False, required=False)
    user_analysis_page  = forms.BooleanField(initial= False, required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count():
            raise forms.ValidationError(u"{} already exists".format(email))
        return email


class UpdateSubscriberForm(forms.Form):
    name            =   forms.CharField(max_length=256)
    timezone        =   forms.ChoiceField(choices=TIMEZONES, initial="Asia/Kolkata")
    pagepermin      =   forms.IntegerField(initial = 0)
    pagepersess     =   forms.IntegerField(initial = 0)
    sesslength      =   forms.IntegerField(initial = 0)
    status          =   forms.IntegerField(initial = 1)
    phone1          =   forms.CharField(max_length = 75)
    phone2          =   forms.CharField(max_length = 75, required=False)
    address1        =   forms.CharField(widget = forms.Textarea, max_length = 500)
    address2        =   forms.CharField(widget = forms.Textarea, max_length = 500,required = False)
    mode            =   forms.ChoiceField(choices=SUBSCRIBER_MODE, initial="Active")

    r_browserIntgrity       = forms.ModelChoiceField(ResponseCode.objects.filter(id__in = (0, 2, )))
    r_httpRequestIntegrity  = forms.ModelChoiceField(ResponseCode.objects.filter(id__in = (0, 2, )))
    r_Aggregator            = forms.ModelChoiceField(ResponseCode.objects.filter(id__in = (0, 2, )))
    r_behaviourIntegrity    = forms.ModelChoiceField(ResponseCode.objects.filter(id__in = (0, 2, )))
    r_Pagepermin            = forms.ModelChoiceField(ResponseCode.objects.filter(id__in = (0, 2, )))

    # Page permissions
    ip_analysis_page    = forms.BooleanField(initial= True, required=False)
    ip_access_page      = forms.BooleanField(initial= True, required=False)
    user_access_page    = forms.BooleanField(initial= False, required=False)
    user_analysis_page  = forms.BooleanField(initial= False, required=False)


class NewUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=200)
    privilege = forms.ChoiceField(choices=USER_PRIVILEGES,
                                  widget=forms.RadioSelect())
    subscriber = forms.ModelChoiceField(
        queryset=Subscriber.objects.all().order_by('name'))


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError("Email {} already exists".format(email))
        return email


class DeActivateUserForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True, is_staff=False).all().\
        order_by('email'))


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=200)


class DeActivateSubscriberForm(forms.Form):
    subscriber = forms.ModelChoiceField(
        queryset=Subscriber.objects.filter(~Q(status=0)).all())


class ReActivateSubscriberForm(forms.Form):
    subscriber = forms.ModelChoiceField(
        queryset=Subscriber.objects.filter(Q(status=0)).all())


class EditSubscriberForm(forms.Form):
    subscriber = forms.ModelChoiceField(
        queryset=Subscriber.objects.all())


class SupportSubscriberReportForm(forms.Form):
    subscriber = forms.ModelChoiceField(
        queryset=Subscriber.objects.filter(~Q(status=0)).all())
    reports = forms.ChoiceField(choices=get_report_choices())
