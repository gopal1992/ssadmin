# -*- coding: utf-8 -*-

import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import (
    password_reset, password_reset_confirm, password_reset_complete)
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.http import require_http_methods

from customer_support.service import send_new_user_email
from ip_analysis.models import UserSubscriber
from service_layer.page_authorization import get_authorized_pages
from utils.account import (get_subscriber_decorator,
                           is_admin, is_shield_square_user,
    is_demo_user_account)
from utils.email import send_templated_email

from .forms import (NewUserForm,
                    TimeZoneForm,
                    DeleteUserForm,
                    LoginForm,
                    ForgotPasswordForm)
from .services import (update_timezone_for_subscriber,
                       create_user_without_password,
                       delete_user_by_email,
                       grant_privilege,
                       modify_privilege,
                       get_user)


### Login
@require_http_methods(["POST", "GET"])
def user_login(request):
    if request.user.is_authenticated():
        return redirect(reverse('ip_analysis.view_traffic_analysis'))

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        next = request.REQUEST.get('next')
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if is_shield_square_user(user) or user.is_staff:
                        request.session['is_support'] = True
                        return redirect(reverse('support.dashboard'))
                    if next:
                        return redirect(next)
                    return redirect(reverse('ip_analysis.view_traffic_analysis'))
                else:
                    messages.error(request,
                             'User is not active or not found')
            else:
                messages.error(request,
                             'Invalid email or password')
            return render(request, "login.html",
                              {'form': form,
                               "error": "User is not active or not found"})

        return render(request, "login.html", {'form': form})
    return render(request, "login.html", {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request,
                     "Successfully logged out")
    return redirect(reverse('accounts.login'))

@require_http_methods(["POST", "GET"])
def forgot_password(request):
    form = ForgotPasswordForm()

    if request.method == "POST":
        form = ForgotPasswordForm(data=request.POST)
        if form.is_valid():
            from_email = form.cleaned_data['email']
            messages.success(request,
                             "Password reset link successfully sent")

            kwargs = {
                'post_reset_redirect' :reverse('accounts.password_reset_done'),
                'email_template_name': 'password_reset_email.html',
                'subject_template_name' : 'email_subject/password_reset_subject.txt',
            }
#             Custom Subject for Forgot Password E-mail
            return password_reset(request,
                                  from_email=settings.EMAIL_HOST_USER,
                                  **kwargs)
        return render(request, "forgot_password.html", {'form': form})
    return render(request, "forgot_password.html",{'form': form})

def custom_password_reset_done(request, *args, **kwargs):
    return render(request, 'password_reset_done.html')

def custom_password_reset_confirm(request, uidb36, token):
    response = password_reset_confirm(
        request,
        uidb64=uidb36,
        token=token,
        template_name='password_reset_confirm.html',
        post_reset_redirect=reverse('accounts.password_reset_complete')
    )
    UserModel = get_user_model()
    uid = urlsafe_base64_decode(uidb36)
    user = UserModel._default_manager.get(pk=uid)
    send_templated_email(label="password_reset_complete",
                         to=user.email,
                         context={'user_name':get_user(user.email)})

    return response

def custom_password_reset_complete(request, *args, **kwargs):
    response = password_reset_complete(request,
                                       template_name='password_reset_complete.html')
    return response

### Admin section
@require_http_methods(["POST"])
@login_required
@user_passes_test(is_admin)
@get_subscriber_decorator
def update_timezone(request, subscriber):
    form = TimeZoneForm(request.POST)
    if form.is_valid():
        timezone = form.cleaned_data['timezone']
        if update_timezone_for_subscriber(subscriber, timezone):
            msg = u"You have updated timezone to {}".format(timezone)
            send_templated_email(label="user_management",
                                 to=request.user.email,
                                 context={'user_name':request.user,'msg': msg})
            data = {'result': True}
            messages.success(request,
                             u"Time Zone updated")
        else:
            data = {'result': False,
                    'errors': [u"Unable to update Time Zone to {}".format(timezone)]
            }
    else:
        data = {'result': False,
                'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["POST"])
@login_required
@user_passes_test(is_admin)
@get_subscriber_decorator
def new_user(request, subscriber):
    form = NewUserForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        privilege = form.cleaned_data['privilege']
        user = create_user_without_password(email)
        if user:
            grant_privilege(user, privilege)
            UserSubscriber.objects.create(user=user, subscriber=subscriber)
            msg = u"You have created new user {} in ShieldSquare system".format(user.email)
            send_templated_email(label="user_management",
                                 to=request.user.email,
                                 context={'user_name':request.user,'msg': msg})
            send_new_user_email(request, user)
            data = {'result': True}
            messages.success(request,
                             'User {} successfully added'.format(email))
        else:
            data = {'result': False,
                    'errors': [u'User {} already exists'.format(email)]}
    else:
        data = {'result': False,
                'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["POST"])
@login_required
@user_passes_test(is_admin)
@get_subscriber_decorator
def edit_user(request, subscriber):
    form = NewUserForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        privilege = form.cleaned_data['privilege']

        user = get_user(email)
        if user:
            modify_privilege(user, privilege)

            privilege_old = 'Normal User'
            if privilege == 'user':
                privilege_old = 'Admin'
                privilege = 'Normal User'
            else :
                privilege = 'Admin'

            msg = u"The privilege for user '{}' is changed from '{}' to '{}'".format(
                user.email, privilege_old, privilege)
            send_templated_email(label="user_management",
                                 to=request.user.email,
                                 context={'user_name': request.user, 'msg': msg})
            data = {'result': True}

            messages.success(request,
                             u"The privilege for user '{}' is changed from '{}' to '{}'".
                             format(email, privilege_old, privilege))
        else:
            data = {'result': False,
                    'errors': [u'Cannot locate User with {}'.format(email)]}
    else:
        data = {'result': False,
                'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["POST"])
@login_required
@user_passes_test(is_admin)
@get_subscriber_decorator
def delete_user(request, subscriber):
    form = DeleteUserForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = delete_user_by_email(email)
        if user:
            msg = u"You have deleted user {}".format(email)
            send_templated_email(label="user_management",
                                 to=request.user.email,
                                 context={'user_name':request.user,'msg': msg})
            data = {'result': True}
            messages.success(request,
                             'User {} successfully deleted'.format(email))
        else:
            data = {'result': False,
                    'errors': [u'Oops. Cannot delete User {}'.format(email)]}
    else:
        data = {'result': False,
                'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["GET"])
@login_required
@user_passes_test(is_admin)
@get_subscriber_decorator
def user_management(request, subscriber):
    user_form = NewUserForm()
    timezone_form = TimeZoneForm()
    default_timezone = timezone_form.fields['timezone'].initial
    timezone_form.fields['timezone'].initial = subscriber.timezone or \
                                               default_timezone
    all_users = subscriber.usersubscriber_set.all()
    is_demo_user    = is_demo_user_account(request.user)
    authorized_page_list = get_authorized_pages(subscriber)
    users = []
    if is_demo_user:
        for user in all_users:
            if is_demo_user_account(user.user):
                users.append(user)
    else:
        for user in all_users:
            if not is_demo_user_account(user.user):
                users.append(user)

    return render(request, "user_management.html",
                  {'user_form'      : user_form,
                   'timezone_form'  : timezone_form,
                   'users'          : users,
                   'can_edit'       : True,
                   'is_demo_user'   : is_demo_user,
                   'auth_pages'     : authorized_page_list})
