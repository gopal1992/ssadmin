from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from form_layer.registration import RegistrationForm, ResendVerficationLink
from service_layer.registration import register_a_new_subscriber, \
    verifying_registration_process, resend_verification_link_process


@require_http_methods(['GET','POST'])
def registration_process(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            res_form = register_a_new_subscriber(request, form)
            if res_form == 1:
                return render(request, 'pending_verfication.html', {'user_name':form.cleaned_data['email'],})
            return render(request, 'registration.html', {'form':form, 'error':res_form})
    return render(request, 'registration.html', {'form':form,})

@require_http_methods(['GET'])
def verifying_registration(request, activation_link):
    user, verification, password  = verifying_registration_process(request, activation_link)
    if verification:
        user = authenticate(username=user.username, password=password)
        if user.is_active:
            if user is not None:
                login(request, user)
                return render(request, 'getting_started.html', {'first_time_login':True})
        return render(request, 'login.html', {'error':'User is currently disabled please contact ShieldSquare administrator'})
    return render(request, 'getting_started.html', {'error':'Please verify the integration link'})

@require_http_methods(['GET','POST'])
def resend_verification_link(request):
    form = ResendVerficationLink()
    if request.method == 'POST':
        form = ResendVerficationLink(request.POST)
        if form.is_valid():
            res_form = resend_verification_link_process(request, form)
            if res_form == 1:
                return render(request, 'pending_verfication.html', {'user_name':form.cleaned_data['email'],})
            return render(request, 'resend_verification.html', {'form':form, 'error':res_form})
    return render(request, 'resend_verification.html', {'form':form,})
