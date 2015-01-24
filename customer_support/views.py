# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView

from accounts.services import (create_user_without_password,
                               grant_privilege)
from dal.registration import get_list_latest_internal_sid_subscribers
from ip_analysis.models import UserSubscriber, Subscriber
from service_layer.registration import get_unique_external_sid
from user_analysis.models import SubscriberPageAuth, PagesList, PageAuthAction
from utils.account import ShieldSquareUserMixin
from utils.email import send_templated_email

from .forms import (NewSubscriberForm,
                    UpdateSubscriberForm,
                    EditSubscriberForm,
                    NewUserForm,
                    DeActivateSubscriberForm,
                    ReActivateSubscriberForm,
                    SupportSubscriberReportForm,)
from .service import send_new_user_email


# Create your views here.
class NewUserView(ShieldSquareUserMixin, FormView):
    form_class = NewUserForm
    template_name = 'new_user.html'

    def send_email(self, email):
        msg = u"You have created a new user {}".format(email)
        send_templated_email(label="customer_support",
                             to=self.request.user.email,
                             context={'user_name':self.request.user,'msg': msg})

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        privilege = form.cleaned_data['privilege']
        subscriber = form.cleaned_data['subscriber']
        user = create_user_without_password(email, username)
        if user:
            grant_privilege(user, privilege)
            UserSubscriber.objects.create(user=user, subscriber=subscriber)
            self.send_email(email)
            # comes from service.py
            send_new_user_email(self.request, user)
            messages.success(self.request,
                             u"{} successfully created.".format(email))
        return render(self.request, self.template_name)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class NewSubscriberView(ShieldSquareUserMixin, FormView):
    form_class = NewSubscriberForm
    template_name = "new_subscriber.html"

    def send_email(self, name):
        msg = u"You have created a new subscriber {}".format(name)
        return send_templated_email(label="customer_support",
                                    to=self.request.user.email,
                                    context={'user_name':self.request.user,'msg': msg})

    def form_valid(self, form):
        subscriber = form.save(commit=True)
        self.send_email(subscriber.name)
        user = create_user_without_password(subscriber.email)
        if user:
            send_new_user_email(self.request, user)
            grant_privilege(user, "admin")
            UserSubscriber.objects.create(user=user, subscriber=subscriber)

            messages.success(
                self.request,
                u"Successfully created subscriber {}".format(subscriber.name)
            )
        else:
            messages.error(
                self.requet,
                u"Unable to create user {}".format(subscriber.email)
            )
            return render(self.request, self.template_name)
        return redirect(reverse('support.dashboard'))


class UpdateSubscriberView(ShieldSquareUserMixin, UpdateView):
    model = Subscriber
    form_class = UpdateSubscriberForm
    template_name = "update_subscriber.html"

    def send_email(self, name):
        msg = u"You have updated subscriber {} details".format(name)
        return send_templated_email(label="customer_support",
                                    to=self.request.user.email,
                                    context={'user_name':self.request.user,'msg': msg})

    def form_valid(self, form):
        subscriber = form.save(commit=True)
        self.send_email(subscriber.name)
        messages.success(self.request,
                         u"Successfully edited subscriber {}".format(
                             subscriber.name))
        return redirect(reverse('support.dashboard'))


class EditSubscriberView(ShieldSquareUserMixin, FormView):
    # view to select to subscriber actual update happens in UpdateSubscriberView
    form_class = EditSubscriberForm
    template_name = "edit_subscriber.html"

    def form_valid(self, form):
        subscriber = form.cleaned_data['subscriber']
        return redirect(reverse('support.update_subscriber',
                                kwargs={'pk': subscriber.internal_sid}))


class DeActivateSubscriberView(ShieldSquareUserMixin, FormView):
    form_class = DeActivateSubscriberForm
    template_name = "deactivate_subscriber.html"

    def send_email(self, name):
        msg = u"You have disabled the subscriber {}".format(name)
        return send_templated_email(label="customer_support",
                                    to=self.request.user.email,
                                    context={'user_name':self.request.user,'msg': msg})

    def deactivate_all_associated_users(self, subscriber):
        for user_subscriber in UserSubscriber.objects.filter(subscriber=subscriber):
            user_subscriber.user.is_active = False
            user_subscriber.user.save()

    def form_valid(self, form):
        subscriber = form.cleaned_data['subscriber']
        subscriber.status = 0
        subscriber.save()
        self.deactivate_all_associated_users(subscriber)
        messages.success(self.request,
                         u"{} is disabled".format(subscriber.name))
        self.send_email(subscriber.name)
        return redirect(reverse('support.dashboard'))


class ReActivateSubscriberView(ShieldSquareUserMixin, FormView):
    form_class = ReActivateSubscriberForm
    template_name = "reactivate_subscriber.html"

    def send_email(self, name):
        msg = u"You have enabled the subscriber {}".format(name)
        return send_templated_email(label="customer_support",
                                    to=self.request.user.email,
                                    context={'user_name':self.request.user,'msg': msg})

    def deactivate_all_associated_users(self, subscriber):
        for user_subscriber in UserSubscriber.objects.filter(subscriber=subscriber):
            user_subscriber.user.is_active = True
            user_subscriber.user.save()

    def form_valid(self, form):
        subscriber = form.cleaned_data['subscriber']
        subscriber.status = 1
        subscriber.save()
        self.deactivate_all_associated_users(subscriber)
        messages.success(self.request,
                         u"{} is enabled".format(subscriber.name))
        self.send_email(subscriber.name)
        return redirect(reverse('support.dashboard'))


class SupportSubscriberReportView(ShieldSquareUserMixin, FormView):
    form_class = SupportSubscriberReportForm
    template_name = "support_report.html"

    def form_valid(self, form):
        subscriber = form.cleaned_data['subscriber']
        self.request.session['sid'] = subscriber.internal_sid
        self.request.session['subscriber_name'] = subscriber.name
        report_url = form.cleaned_data['reports']
        return redirect(report_url)


class DashboardView(ShieldSquareUserMixin, TemplateView):
    template_name = "support_dashboard.html"

@require_http_methods(["GET", "POST"])
def add_new_subscriber(request):
    form = NewSubscriberForm()
    if request.method == 'GET':
        return render(request, 'new_subscriber.html', {'form' : form})
    form = NewSubscriberForm(request.POST)
    if form.is_valid():
        latest_internal_sid     =   get_list_latest_internal_sid_subscribers()
        external_sid            =   get_unique_external_sid()
        new_external_sid        =   str(external_sid[0])
        new_sb_external_sid     =   str(external_sid[1])
        sid = Subscriber.objects.create(internal_sid           = latest_internal_sid + 2,
                                        external_sid           = new_external_sid,
                                        mini_uuid              = new_external_sid.split('-')[3],
                                        name                   = form.cleaned_data['name'],
                                        site_url               = form.cleaned_data['site_url'],
                                        address1               = form.cleaned_data['address1'],
                                        address2               = form.cleaned_data['address2'],
                                        phone1                 = form.cleaned_data['phone1'],
                                        phone2                 = form.cleaned_data['phone2'],
                                        email                  = form.cleaned_data['email'],
                                        status                 = form.cleaned_data['status'],
                                        timezone               = form.cleaned_data['timezone'],
                                        r_Pagepermin           = form.cleaned_data['r_Pagepermin'],
                                        r_browserIntgrity      = form.cleaned_data['r_browserIntgrity'],
                                        r_httpRequestIntegrity = form.cleaned_data['r_httpRequestIntegrity'],
                                        r_Aggregator           = form.cleaned_data['r_Aggregator'],
                                        r_behaviourIntegrity   = form.cleaned_data['r_behaviourIntegrity'],
                                        mode                   = form.cleaned_data['mode'],
                                        sb_internal_sid           = latest_internal_sid + 3,
                                        sb_external_sid        = new_sb_external_sid,
                                        sb_mini_uuid           = new_sb_external_sid.split('-')[3]
                                        )

        SubscriberPageAuth.objects.create(sid     = sid,
                                          page_id = PagesList.objects.get(id = 1),
                                          auth_id = PageAuthAction.objects.get(id = 1 if form.cleaned_data['user_access_page'] else 2))
        SubscriberPageAuth.objects.create(sid     = sid,
                                          page_id = PagesList.objects.get(id = 2),
                                          auth_id = PageAuthAction.objects.get(id = 1 if form.cleaned_data['user_analysis_page'] else 2))
        SubscriberPageAuth.objects.create(sid     = sid,
                                          page_id = PagesList.objects.get(id = 3),
                                          auth_id = PageAuthAction.objects.get(id = 1 if form.cleaned_data['ip_analysis_page'] else 2))
        SubscriberPageAuth.objects.create(sid     = sid,
                                          page_id = PagesList.objects.get(id = 4),
                                          auth_id = PageAuthAction.objects.get(id = 1 if form.cleaned_data['ip_access_page'] else 2))

        # Email
        msg = u"You have created a new subscriber {}".format(sid.name)
        send_templated_email(label="customer_support",
                             to=request.user.email,
                             context={'user_name':request.user,'msg': msg})
        user = create_user_without_password(sid.email)
        if user:
            send_new_user_email(request, user)
            grant_privilege(user, "admin")
            UserSubscriber.objects.create(user=user, subscriber=sid)

            messages.success(
                request,
                u"Successfully created subscriber {}".format(sid.name)
            )
        else:
            messages.error(
                request,
                u"Unable to create user {}".format(sid.email)
            )
            return render(request, 'new_subscriber.html')
        return redirect(reverse('support.dashboard'))
    return render(request, 'new_subscriber.html', {'form' : form})

@require_http_methods(["GET", "POST"])
def update_existing_subscriber(request, pk):
    form = UpdateSubscriberForm()
    sid     = Subscriber.objects.get(pk = pk)
    if request.method == 'GET':
        user_access_page    = SubscriberPageAuth.objects.get(sid=sid, page_id = PagesList.objects.get(id = 1))
        user_analysis_page  = SubscriberPageAuth.objects.get(sid=sid, page_id = PagesList.objects.get(id = 2))
        ip_access_page      = SubscriberPageAuth.objects.get(sid=sid, page_id = PagesList.objects.get(id = 3))
        ip_analysis_page    = SubscriberPageAuth.objects.get(sid=sid, page_id = PagesList.objects.get(id = 4))

        form    = UpdateSubscriberForm( initial = {
                                                'name'                   : sid.name,
                                                'address1'               : sid.address1,
                                                'address2'               : sid.address2,
                                                'phone1'                 : sid.phone1,
                                                'phone2'                 : sid.phone2,
                                                'status'                 : sid.status,
                                                'timezone'               : sid.timezone,
                                                'pagepermin'             : sid.pagepermin,
                                                'pagepersess'            : sid.pagepersess,
                                                'sesslength'             : sid.sesslength,
                                                'r_Pagepermin'           : sid.r_Pagepermin,
                                                'r_pagepersess'          : sid.r_pagepersess,
                                                'r_sesslength'           : sid.r_sesslength,
                                                'r_browserIntgrity'      : sid.r_browserIntgrity,
                                                'r_httpRequestIntegrity' : sid.r_httpRequestIntegrity,
                                                'r_Aggregator'           : sid.r_Aggregator,
                                                'r_behaviourIntegrity'   : sid.r_behaviourIntegrity,
                                                'mode'                   : sid.mode,
                                                'user_access_page'       : True if user_access_page.auth_id.id==1 else False,
                                                'user_analysis_page'     : True if user_analysis_page.auth_id.id==1 else False,
                                                'ip_access_page'         : True if ip_access_page.auth_id.id==1 else False,
                                                'ip_analysis_page'       : True if ip_analysis_page.auth_id.id==1 else False,
                                                })
        return render(request, 'update_subscriber.html', {'form'         : form,
                                                          'internal_sid' : sid.internal_sid,
                                                          'external_sid' : sid.external_sid,})

    form = UpdateSubscriberForm(request.POST)
    if form.is_valid():
        sid = Subscriber.objects.get(pk = pk)
        sid.name                   = form.cleaned_data['name']
        sid.address1               = form.cleaned_data['address1']
        sid.address2               = form.cleaned_data['address2']
        sid.phone1                 = form.cleaned_data['phone1']
        sid.phone2                 = form.cleaned_data['phone2']
        sid.status                 = form.cleaned_data['status']
        sid.timezone               = form.cleaned_data['timezone']
        sid.r_Pagepermin           = form.cleaned_data['r_Pagepermin']
        sid.r_browserIntgrity      = form.cleaned_data['r_browserIntgrity']
        sid.r_httpRequestIntegrity = form.cleaned_data['r_httpRequestIntegrity']
        sid.r_Aggregator           = form.cleaned_data['r_Aggregator']
        sid.r_behaviourIntegrity   = form.cleaned_data['r_behaviourIntegrity']
        sid.mode                   = form.cleaned_data['mode']
        sid.save()

        user_access_page   = SubscriberPageAuth.objects.get(sid       = sid,
                                                            page_id   = PagesList.objects.get(id = 1))
        user_analysis_page = SubscriberPageAuth.objects.get(sid       = sid,
                                                            page_id   = PagesList.objects.get(id = 2))
        ip_access_page     = SubscriberPageAuth.objects.get(sid       = sid,
                                                            page_id   = PagesList.objects.get(id = 3))
        ip_analysis_page   = SubscriberPageAuth.objects.get(sid       = sid,
                                                            page_id   = PagesList.objects.get(id = 4))
        user_access_page.auth_id      = PageAuthAction.objects.get(auth_action = 1 if form.cleaned_data['user_access_page'] else 0)
        user_analysis_page.auth_id    = PageAuthAction.objects.get(auth_action = 1 if form.cleaned_data['user_analysis_page'] else 0)
        ip_access_page.auth_id        = PageAuthAction.objects.get(auth_action = 1 if form.cleaned_data['ip_access_page'] else 0)
        ip_analysis_page.auth_id      = PageAuthAction.objects.get(auth_action = 1 if form.cleaned_data['ip_analysis_page'] else 0)

        user_access_page.save()
        user_analysis_page.save()
        ip_access_page.save()
        ip_analysis_page.save()

        # Email
        msg = u"You have updated subscriber {} details".format(sid.name)
        send_templated_email(label="customer_support",
                             to=request.user.email,
                             context={'user_name':request.user,'msg': msg})
        messages.success(request, u"Successfully edited subscriber {}".format(sid.name))
        return redirect(reverse('support.dashboard'))
    return render(request, 'update_subscriber.html', {'form'         : form,
                                                      'internal_sid' : sid.internal_sid,
                                                      'external_sid' : sid.external_sid,})