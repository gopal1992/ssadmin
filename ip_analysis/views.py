# -*- coding: utf-8 -*-

from datetime import timedelta
import datetime
import json

from dateutil import rrule
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ip_analysis.forms import IpAccessStatusForm, IpAccessStatusDeleteForm, \
    IpAccessStatusSearchForm, IpAccessStatusWithNoInputForm, \
    IpAnalysisSearchForm, IpActionUpdateForm
from ip_analysis.models import IpDetails, IpAddressAccessList, IpAnalysis, \
    RulesSummary, IpActions, ResponseCode, IpStatus
from ip_analysis.service import configuration_ip_access_list, \
    ip_analysis_details as ip_analysis_details_service, \
    traffic_analysis as ta_service
from ip_analysis.service.ip_analysis_details import convert_date_specific_to_timezone, \
    individual_ip_address_details, update_ip_action, convert_tz_tailored_dates_in_list_to_displayable_date, \
    optimize_data_based_on_number_of_days, hourly_date_available_message_display
from service_layer.page_authorization import get_authorized_pages
from utils.account import get_subscriber_decorator, is_admin, is_normal_user, \
    is_monitor_mode, is_demo_user_account
from utils.constants import ACCESS_STATUS_DENY, ACCESS_STATUS_ALLOW, \
    ACCESS_STATUS_MAP
from utils.decorator import access_to_page

from .forms import (PagesPerMinuteRulesForm,
                    PagesPerSessionRulesForm,
                    SessionLengthRulesForm,
                    BrowserIntegrityCheckForm,
                    HTTPRequestIntegrityCheckForm,
                    AggregatorCheckForm,
                    BehaviourIntegrityCheckForm
                    )
from .service import (update_pages_per_session,  # @UnresolvedImport
                      update_session_length,  # @UnresolvedImport
                      update_bot_category_check,  # @UnresolvedImport
                      complete_traffic_analysis,
                      complete_ip_analysis,
                      get_n_displayble_traffic_details,
                      write_to_excel_traffic_analysis,
                      write_to_excel_ip_analysis)


# from ip_analysis.service.traffic_analysis import get_missing_data_in_given_date_range
DELAY_DAYS = settings.SYNC_DELAY


# IP Analysis
@require_http_methods(["POST"])
@login_required
@get_subscriber_decorator
def update_action_for_ip_analysis(request, subscriber):
    form = IpActionUpdateForm(request.POST)
    if form.is_valid():
        ip_address = form.cleaned_data['ip_address']
        action = form.cleaned_data['action']
        expiry_date    = form.cleaned_data['expiry_date']
        action, expiry_date = update_ip_action(subscriber, action, expiry_date, ip_address)
#         # Email
#         user = request.user
#         if user.email:
#             send_templated_email(
#                 label="ip_analysis",
#                 to=user.email,
#                 context={'user_name':user,'action': action, }
#             )
#         else:
#             # Fail silently for now
#             pass
        data = {'action'        : action,
                'expiry_date'   : expiry_date,
                'result'        : True,
                'errors'        : None}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(data, mimetype='application/json')

# Rate Limiting Rules
@require_http_methods(["POST"])
@login_required
@get_subscriber_decorator  # @UndefinedVariable
def add_pages_per_minute(request, subscriber):
    form = PagesPerMinuteRulesForm(request.POST)
    if form.is_valid():
        action = form.cleaned_data['action']
        update_bot_category_check(subscriber, action, "rate_limiting")
#         user = request.user
#         if user.email:
#             send_templated_email(
#                 label="bot_response",
#                 to=user.email,
#                 context={'user_name':user,'action': 'rate limiting check'}
#             )
#         else:
#             # Fail silently for now
#             pass
        data = {'result': True,
                'errors': None}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["POST"])
@login_required
@get_subscriber_decorator
def add_pages_per_session(request, subscriber):
    form = PagesPerSessionRulesForm(request.POST)
    if form.is_valid():
        pages_per_session = form.cleaned_data['pages_per_session']
        action = form.cleaned_data['action']
        try:
            if update_pages_per_session(subscriber, pages_per_session, action):
#                 user = request.user
#                 if user.email:
#                     send_templated_email(
#                         label="bot_response",
#                         to=user.email,
#                         context={'user_name':user,'action': 'pages per session'}
#                     )
#                 else:
#                     # Fail silently for now
#                     pass

                # Send Email
                data = {'result': True,
                        'errors': None}
        except:
            msg = u"Oops. Something went wrong. Please try after some time"
            data = {'result': False,
                    'errors': msg}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["POST"])
@login_required
@get_subscriber_decorator
def add_session_length(request, subscriber):
    form = SessionLengthRulesForm(request.POST)
    if form.is_valid():
        session_length = form.cleaned_data['session_length']
        action = form.cleaned_data['action']
        try:
            if update_session_length(subscriber, session_length, action):
#                 user = request.user
#                 if user.email:
#                     send_templated_email(
#                         label="bot_response",
#                         to=user.email,
#                         context={'user_name':user,'action': 'session length'}
#                     )
#                 else:
#                     # Fail silently for now
#                     pass

                # Send Email
                data = {'result': True,
                        'errors': None}
        except:
            msg = u"Oops. Something went wrong. Please try after some time"
            data = {'result': False,
                    'errors': msg}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

# Bot Response Rules
@require_http_methods(["POST"])
@login_required
@get_subscriber_decorator
def add_browser_integrity_check(request, subscriber):
    form = BrowserIntegrityCheckForm(request.POST)
    if form.is_valid():
        action = form.cleaned_data['action']
        update_bot_category_check(subscriber, action, "browser_integrity")
        # Email
#         user = request.user
#         if user.email:
#             status = send_templated_email(  # @UnusedVariable
#                 label="bot_response",
#                 to=[user.email],
#                 context={'user_name':user,'action': 'browser integrity'}
#             )
#         else:
#             # Fail silently for now
#             pass
        data = {'result': True,
                'errors': None}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@get_subscriber_decorator
def add_http_request_integrity_check(request, subscriber):
    form = HTTPRequestIntegrityCheckForm(request.POST)
    if form.is_valid():
        action = form.cleaned_data['action']
        update_bot_category_check(subscriber, action, "http_request")
        # Email
#         user = request.user
#         if user.email:
#             send_templated_email(
#                 label="bot_response",
#                 to=user.email,
#                 context={'user_name':user,'action': 'HTTP request integrity'}
#             )
#         else:
#             # Fail silently for now
#             pass
        data = {'result': True,
                'errors': None}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@get_subscriber_decorator
def add_aggregator_bot_traffic_check(request, subscriber):
    form = AggregatorCheckForm(request.POST)
    if form.is_valid():
        action = form.cleaned_data['action']
        update_bot_category_check(subscriber, action, "aggregator")
        # Email
#         user = request.user
#         if user.email:
#             send_templated_email(
#                 label="bot_response",
#                 to=user.email,
#                 context={'user_name':user,'action': 'aggregator bot traffic'}
#             )
#         else:
#             # Fail silently for now
#             pass
        data = {'result': True,
                'errors': None}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["POST"])
@login_required
@get_subscriber_decorator
def add_behaviour_integrity_check(request, subscriber):
    form = BehaviourIntegrityCheckForm(request.POST)
    if form.is_valid():
        action = form.cleaned_data['action']
        update_bot_category_check(subscriber, action, "behaviour")
        # Email
#         user = request.user
#         if user.email:
#             send_templated_email(
#                 label="bot_response",
#                 to=user.email,
#                 context={'user_name':user,'action': 'behaviour integrity check'}
#             )
#         else:
#             # Fail silently for now
#             pass
        data = {'result': True,
                'errors': None}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(data, mimetype='application/json')

# Main view page for Bot Response List
@require_http_methods(["GET"])
@login_required
# @user_passes_test(is_admin)
@get_subscriber_decorator
def view_bot_response(request, subscriber):
    pages_per_minute_form = PagesPerMinuteRulesForm()
    pages_per_minute_form.fields['action'].initial = subscriber.r_Pagepermin.id

    pages_per_session_form = PagesPerSessionRulesForm()
    pages_per_session_form.fields['pages_per_session'].initial = subscriber.pagepersess
    pages_per_session_form.fields['action'].initial = subscriber.r_pagepersess.id

    session_length_form = SessionLengthRulesForm()
    session_length_form.fields['session_length'].initial = subscriber.sesslength
    session_length_form.fields['action'].initial = subscriber.r_sesslength.id

    browser_integrity_form = BrowserIntegrityCheckForm()
    browser_integrity_form.fields['action'].initial = subscriber.r_browserIntgrity.id

    http_request_integrity_form = HTTPRequestIntegrityCheckForm()
    http_request_integrity_form.fields['action'].initial = subscriber.r_httpRequestIntegrity.id

    aggregator_check_form = AggregatorCheckForm()
    aggregator_check_form.fields['action'].initial = subscriber.r_Aggregator.id

    behaviour_integrity_form = BehaviourIntegrityCheckForm()
    behaviour_integrity_form.fields['action'].initial = subscriber.r_behaviourIntegrity.id

    can_edit        = any(is_admin(request.user))
    is_monitor      = is_monitor_mode(subscriber,request.user)
    is_demo_user    = is_demo_user_account(request.user)
    authorized_page_list = get_authorized_pages(subscriber)

    return render(request,
                  'bot_response.html',
                  {'pages_per_minute_form'      : pages_per_minute_form,
                   'pages_per_session_form'     : pages_per_session_form,
                   'session_length_form'        : session_length_form,
                   'browser_integrity_form'     : browser_integrity_form,
                   'http_request_integrity_form': http_request_integrity_form,
                   'aggregator_check_form'      : aggregator_check_form,
                   'behaviour_integrity_form'   : behaviour_integrity_form,
                   'subscriber'                 : subscriber,
                   'can_edit'                   : can_edit,
                   'is_demo_user'               : is_demo_user,
                   'is_monitor'                 : is_monitor,
                   'auth_pages'                 : authorized_page_list})

####################### IP Access List ########################################

@require_http_methods(["POST"])
@login_required
@get_subscriber_decorator
def add_ip_access_status(request, subscriber):
    form = IpAccessStatusForm(request.POST)
    if form.is_valid():
        # Call service layer to persist
        result = configuration_ip_access_list.add_ip_access_status(form.data['ip_address_add'],
                                                                    ACCESS_STATUS_MAP[True], # Hidden fields won't be available in cleaned_data
                                                                    subscriber)
        if result['created']:
            messages.success(request, "Successfully added the IP Address '{}' to whitelist.".format(form.cleaned_data['ip_address_add']))
        else: # Record is already available and updated
            messages.success(request, "Successfully whitelisted the IP Address '{}'." .format(form.cleaned_data['ip_address_add']))

        try:
            ipdetails = IpDetails.objects.get(ip_address = form.cleaned_data['ip_address_add'])
            ipactions = IpActions.objects.get(sid=subscriber, ip_address=ipdetails)

            ipactions.expiry_date = datetime.date.today() + timedelta(days=365.25 * 10)
            ipactions.status      = IpStatus.objects.filter(id=0)[0]
            ipactions.action      = ResponseCode.objects.filter(id=0)[0]
            ipactions.save()
        except ObjectDoesNotExist:
            pass

#         user = request.user
#         if user.email:
#             send_templated_email(
#                 label="ip_access",
#                 to=user.email,
#                 context={"action": "whitelisted", "ip": form.cleaned_data['ip_address_add']})
#         else:
#             # Fail silently for now
#             pass

        data = {'result': True,}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    # end if
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["POST"])
@login_required
@get_subscriber_decorator
def delete_ip_access_status(request, subscriber, instance_id):
    form = IpAccessStatusDeleteForm(request.POST)
    if form.is_valid():
        ip_address = IpAddressAccessList.objects.get(pk = instance_id).ipaddress
        try:
            ip_details  = IpDetails.objects.get(ip_address = ip_address)
            ipactions  = IpActions.objects.get(sid=subscriber, ip_address = ip_details)

            ipactions.expiry_date = datetime.date.today()
            ipactions.status      = IpStatus.objects.filter(id=1)[0]
            ipactions.action      = ResponseCode.objects.filter(id=0)[0]
            ipactions.save()
        except ObjectDoesNotExist:
            pass

        # Call service layer to delete
        deleted = configuration_ip_access_list.delete_ip_access_status(instance_id)
        data = {'result': True,}
        if deleted:
            messages.success(request, "Successfully deleted the IP Address '{}' from Whitelist".format(ip_address))

#             # Send E-Mail Notification
#             user = request.user
#             if user.email:
#                 send_templated_email(
#                     label="ip_access",
#                     to=user.email,
#                     context={"action": "deleted", "ip": ip_address})
#             else:
#                 # Fail silently for now
#                 pass
        else: # Record is already available and updated
            data = {'result': False,
                    'errors': "Failed to delete the IP Address."}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    # end if
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["POST"])
@login_required
@get_subscriber_decorator
def add_ip_access_status_for_ip_analysis(request, subscriber):
    form = IpAccessStatusWithNoInputForm(request.POST)
    if form.is_valid():
        # Call service layer to persist
        created = configuration_ip_access_list.add_ip_access_status(form.data['ip_address'],
                                                                   ACCESS_STATUS_MAP[form.data['access_status']],
                                                                   subscriber)
        # Send E-Mail Notification
        action = ""
        if form.data['access_status'] == ACCESS_STATUS_ALLOW:
            action = "whitelisted"
        elif form.data['access_status'] == ACCESS_STATUS_DENY:
            action = "blacklisted"

#         user = request.user
#         if user.email:
#             send_templated_email(
#                 label="ip_access",
#                 to=user.email,
#                 context={"action": action, "ip": form.data['ip_address']})
#         else:
#             # Fail silently for now
#             pass

        if created:
            messages.success(request, "Successfully {} the IP Address '{}'.".format(action, form.data['ip_address']))
        else: # Record is already available and updated
            messages.success(request, "Successfully {} the IP Address '{}'.".format(action, form.data['ip_address']))
        return HttpResponse(json.dumps({'result': True,}), mimetype='application/json')
    # end if
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["GET"])
@login_required
@get_subscriber_decorator
@access_to_page('IP Access')
def list_ip_access_status(request, subscriber):  # @UndefinedVariable
    page_no =   request.GET.get('page', 1)
    form    =   IpAccessStatusSearchForm(request.GET)

    search_ip_address   = None

    if form.is_valid():
        search_ip_address   = form.cleaned_data['ip_address'].strip()

    # Call service layer to persist
    paginator = Paginator(configuration_ip_access_list.get_ip_access_status_list(subscriber, search_ip_address),15)

    try:
        ip_access_status_list = paginator.page(page_no)
    except PageNotAnInteger:
        ip_access_status_list = paginator.page(page_no)
    except EmptyPage:
        ip_access_status_list = paginator.page(paginator.num_pages)

    ip_access_status_table = [] # List of dicts for HTML rendering
    for ip_access_status in ip_access_status_list:
        try:
            ip_access_status_table.append({ 'id'            :   ip_access_status.pk,
                                            'ip_address'    :   ip_access_status.ipaddress
                                          })
        except ObjectDoesNotExist:
            print ip_access_status.pk
    # Is search requested -> to display the search boxes if no results found in the search
    search = False
    if any([search_ip_address]):
        search = True

    can_edit        = any(is_admin(request.user))
    is_demo_user    = is_demo_user_account(request.user)
    is_monitor      = is_monitor_mode(subscriber,request.user)
    authorized_page_list = get_authorized_pages(subscriber)

    return render(request,
                  'ip_accesslist.html',
                  {
                       'ip_access_status_table'     : ip_access_status_table,
                       'search_from'                : form,
                       'access_status_add_form'     : IpAccessStatusForm(),
                       'access_status_delete_form'  : IpAccessStatusWithNoInputForm(),
                       'ip_access_status_list'      : ip_access_status_list,
                       'is_demo_user'               : is_demo_user,
                       'can_edit'                   : can_edit,
                       'search'                     : search,
                       'is_monitor'                 : is_monitor,
                       'auth_pages'                 : authorized_page_list
                   }
                  )

def get_bad_bot_traffic_details(ip_analysis_detail):
#     total_bad_requests =    ip_analysis_detail.browserIntgrity + \
#                             ip_analysis_detail.httpRequestIntegrity + \
#                             ip_analysis_detail.Aggregator + \
#                             ip_analysis_detail.behaviourIntegrity + \
#                             ip_analysis_detail.Ratelimiting

    bad_bot_traffic_details = {'browserIntgrity' :
                                    {'count'      : ip_analysis_detail['browserIntgrity'],
#                                      'percentage' : ip_analysis_detail.behaviourIntegrity / total_bad_requests * 100
                                    },
                               'httpRequestIntegrity' :
                                    {'count'      : ip_analysis_detail['httpRequestIntegrity'],
#                                      'percentage' : ip_analysis_detail.httpRequestIntegrity / total_bad_requests * 100
                                    },
                               'Aggregator' :
                                    {'count'      : ip_analysis_detail['Aggregator'],
#                                      'percentage' : ip_analysis_detail.Aggregator / total_bad_requests * 100
                                    },
                               'behaviourIntegrity' :
                                    {'count'      : ip_analysis_detail['behaviourIntegrity'],
#                                      'percentage' : ip_analysis_detail.behaviourIntegrity / total_bad_requests * 100
                                    },
                               'Ratelimiting' :
                                    {'count'      : ip_analysis_detail['Ratelimiting'],
#                                      'percentage' : ip_analysis_detail.Ratelimiting / total_bad_requests * 100
                                    },
                                'Totalcount' :
                                    {'count'      : ip_analysis_detail['totalrequests'],
#                                      'percentage' : ip_analysis_detail.Ratelimiting / total_bad_requests * 100
                                    }

                              }
    return bad_bot_traffic_details


def ip_address_clean_or_malicious(ipaddress, subscriber):
    try:
        ip_address_status = IpActions.objects.get(ip_address = ipaddress, sid = subscriber).status
        return "Malicious" if ip_address_status.id == 1  else "Clean"
    except ObjectDoesNotExist:
        return "Clean"

def _get_date_from_timestamp(request, start_date_utc, end_date_utc):

    today = (datetime.datetime.utcnow() - datetime.timedelta(days=DELAY_DAYS)).replace(hour=0,minute=0,second=0)

    if end_date_utc:
        end_date_float = int(end_date_utc) / 1000.0
        end_date = datetime.datetime.fromtimestamp(end_date_float)
        request.session['end_date'] = end_date_float
    else:
        sess_end_date = request.session.get('end_date')
        if sess_end_date:
            end_date = datetime.datetime.fromtimestamp(int(sess_end_date))
        else:
            timestamp = int(today.strftime("%s"))
            end_date = datetime.datetime.fromtimestamp(int(timestamp))

    if start_date_utc:
        start_date_float = int(start_date_utc) / 1000.0
        start_date = datetime.datetime.fromtimestamp(start_date_float)
        request.session['start_date'] = start_date_float

    else:
        sess_start_date = request.session.get('start_date')
        if sess_start_date:
            start_date = datetime.datetime.fromtimestamp(int(sess_start_date))
        else:
            start_date = end_date - datetime.timedelta(days=30)

    return start_date, end_date


def _get_date_from_timestamp_inner(request, start_date_utc, end_date_utc):
    end_date_float = int(end_date_utc) / 1000.0
    end_date = datetime.datetime.fromtimestamp(end_date_float)
    start_date_float = int(start_date_utc) / 1000.0
    start_date = datetime.datetime.fromtimestamp(start_date_float)
    return start_date, end_date

@require_http_methods(["GET"])
@login_required
@get_subscriber_decorator
def get_ip_details_in_specific_range(request, subscriber):  # @UndefinedVariable
    ip_address  = request.GET.get('ip_address')
    start_date  = request.GET.get('date_from')
    end_date    = request.GET.get('date_to')
    ip_details  = IpDetails.objects.filter(ip_address=ip_address)
    ip_address  = ip_details[0].id
    actual_start_date, actual_end_date = _get_date_from_timestamp_inner(request, start_date, end_date)
    start_date, end_date = convert_date_specific_to_timezone(subscriber.timezone,
                                                             actual_start_date,
                                                             actual_end_date)

    diff        = end_date - start_date
    show_time   = True if diff.days < 3 else False
    hourly_message = hourly_date_available_message_display(start_date)
    ip_line_graph_date = [] # Name of list to represent X axis for the Line graph in Detailed IP information
    ip_line_graph_hits = [] # Name of list to represent Y axis for the Line graph in Detailed IP information
    line_graph_ip_object = IpAnalysis.objects.filter(sid = subscriber,
                                                     ipaddress = ip_address,
                                                     dt__range = [start_date, end_date])
    for ips in line_graph_ip_object:
        conv_date       =   str(ips.dt)
        totalrequests   =   json.dumps(ips.totalrequests)
        ip_line_graph_date.append(conv_date)
        ip_line_graph_hits.append(totalrequests)

    ip_line_graph_date = convert_tz_tailored_dates_in_list_to_displayable_date(subscriber.timezone, ip_line_graph_date)
    ip_line_graph_date, ip_line_graph_hits = optimize_data_based_on_number_of_days(ip_line_graph_date, ip_line_graph_hits, show_time)
    single_hour_data   = True if len(ip_line_graph_date) == 1 else False #Checks for entries for a single hour in single day
    data = {'ip_line_graph_date' : ip_line_graph_date,
            'ip_line_graph_hits' : ip_line_graph_hits,
            'single_hour_data'   : single_hour_data,
            'hourly_message'     : hourly_message}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["GET"])
@login_required
@get_subscriber_decorator
@access_to_page('IP Analysis')
def list_ip_analysis_details(request, subscriber):  # @UndefinedVariable
    page_no = request.GET.get('page', 1)

    start_date_utc  = request.GET.get('date_from')
    end_date_utc    = request.GET.get('date_to')

    start_date, end_date = _get_date_from_timestamp(request, start_date_utc, end_date_utc)
    form = IpAnalysisSearchForm(request.GET)

    search_ip_address   = None
    search_country_name = None
    search_isp          = None
    search_city_name    = None

    if form.is_valid():
        search_ip_address   = form.cleaned_data['ip_address'].strip()
        search_country_name = form.cleaned_data['country_name'].strip()
        search_isp          = form.cleaned_data['isp'].strip()
        search_city_name    = form.cleaned_data['city_name'].strip()
        search_status       = form.cleaned_data['status'].strip()

    start_date, end_date = convert_date_specific_to_timezone(subscriber.timezone, start_date, end_date)

    diff        = end_date - start_date
    show_time   = True if diff.days < 3 else False

    # Call service layer to fetch the details
    data = ip_analysis_details_service.get_ip_analysis_details(subscriber,
                                                               search_ip_address,
                                                               search_country_name,
                                                               search_isp,
                                                               search_city_name,
                                                               search_status,
                                                               start_date,
                                                               end_date)

    paginator = Paginator(data, 15)
    ip_analysis_details = None
    try:
        ip_analysis_details = paginator.page(page_no)
    except PageNotAnInteger:
        ip_analysis_details = paginator.page(page_no)
    except EmptyPage:
        ip_analysis_details = paginator.page(paginator.num_pages)

    ip_analysis_details_table = [] # List of dicts for HTML rendering
    for ip_analysis_detail in ip_analysis_details:
        ipaddress = IpDetails.objects.get(pk = ip_analysis_detail['ipaddress'])
        ip_action_form, ip_line_graph_date, ip_line_graph_hits, ip_action, expiry_date, hourly_message = individual_ip_address_details(subscriber,
                                                                               ipaddress.id,
                                                                               start_date,
                                                                               end_date,
                                                                               show_time)
        ip_address_status = ip_address_clean_or_malicious(ipaddress, subscriber)
        single_hour_data   = True if len(ip_line_graph_date) == 1 else False #Checks for entries for a single hour in single day
        ip_analysis_details_dict = {    'id'                      :   0,
                                        'ip_address'              :   ipaddress.ip_address,
                                        'country_name'            :   ipaddress.country_name,
                                        'isp'                     :   ipaddress.isp,
                                        'ip_action_form'          :   ip_action_form,
                                        'ip_action'               :   ip_action,
                                        'expiry_date'             :   expiry_date,
                                        'city_name'               :   ipaddress.city_name,
                                        'bot_hits'                :   ip_analysis_detail['totalrequests'],
                                        'ip_line_graph_date'      :   ip_line_graph_date,
                                        'ip_line_graph_hits'      :   ip_line_graph_hits,
                                        'single_hour_data'        :   single_hour_data,
                                        'ip_address_status'       :   ip_address_status,
                                        'bad_bot_traffic_details' :   get_bad_bot_traffic_details(ip_analysis_detail)
                                    }

        ip_analysis_details_table.append(ip_analysis_details_dict)
    search = False
    if any([search_ip_address, search_country_name, search_isp, search_city_name, search_status]):
        search = True

    can_edit        = any(is_admin(request.user))
    is_monitor      = is_monitor_mode(subscriber,request.user)
    is_demo_user    = is_demo_user_account(request.user)
    authorized_page_list = get_authorized_pages(subscriber)
    return render(request,
                  'ip_analysis.html',
                  {'ip_analysis_details_table'  : ip_analysis_details_table,
                   'search_from'                : form,
                   'ip_analysis_details'        : ip_analysis_details,
                   'can_edit'                   : can_edit,
                   'is_demo_user'               : is_demo_user,
                   'is_monitor'                 : is_monitor,
                   'search'                     : search,
                   'auth_pages'                 : authorized_page_list
                  })

################# Traffic Analysis ######################

def get_base_results_for_traffic_analysis(request, subscriber):
    start_date_utc  = request.GET.get('start_date')
    end_date_utc    = request.GET.get('end_date')

    start_date, end_date = _get_date_from_timestamp(request, start_date_utc, end_date_utc)
    start_date, end_date = convert_date_specific_to_timezone(subscriber.timezone, start_date, end_date)

    diff        = end_date - start_date
    show_time   = False if diff.days > 0 else True
    return complete_traffic_analysis(subscriber, start_date, end_date), show_time, start_date, end_date

def get_base_results_for_ip_analysis(request, subscriber):
    start_date_utc  = request.GET.get('date_from')
    end_date_utc    = request.GET.get('date_to')

    start_date, end_date = _get_date_from_timestamp(request, start_date_utc, end_date_utc)
    return complete_ip_analysis(subscriber, start_date, end_date)

def get_base_results_for_ip_analysis_excel(request, subscriber):
    start_date_utc  = request.GET.get('date_from')
    end_date_utc    = request.GET.get('date_to')
    start_date, end_date = _get_date_from_timestamp(request, start_date_utc, end_date_utc)


    search_ip_address   = None
    search_country_name = None
    search_isp          = None
    search_city_name    = None
    search_status       = None

    start_date, end_date = convert_date_specific_to_timezone(subscriber.timezone, start_date, end_date)
    # Call service layer to fetch the details
    data = ip_analysis_details_service.get_ip_analysis_details(subscriber,
                                                               search_ip_address,
                                                               search_country_name,
                                                               search_isp,
                                                               search_city_name,
                                                               search_status,
                                                               start_date,
                                                               end_date)
    result = {'ip_analysis': data, }
    return result
#     return complete_ip_analysis(subscriber, start_date, end_date)

@require_http_methods(["GET"])
@login_required
@user_passes_test(is_normal_user)
@get_subscriber_decorator
def excel_view_traffic_analysis(request, subscriber):
    # changing any key will affect in multiple places.
    res, show_time, start_date, end_date = get_base_results_for_traffic_analysis(request, subscriber)
    res['traffic_analysis_result'] = get_n_displayble_traffic_details(
        res['traffic_analysis'], n=10, show_time=show_time,
        timezone=subscriber.timezone,
        start_date=start_date,
        end_date=end_date)
    filename = "{}.{}".format("traffic_analysis",
                              "xls")
    excel = write_to_excel_traffic_analysis(res)
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = u'attachment; filename={}'.format(filename)
    excel.save(response)
    return response

@require_http_methods(["GET"])
@login_required
@user_passes_test(is_normal_user)
@get_subscriber_decorator
def excel_view_ip_analysis(request, subscriber):
    # Changing any key will affect in multiple places.
    # Below function is conflicting with time zone convertion, new function was written to rectify the issue
    # res = get_base_results_for_ip_analysis(request, subscriber)
    res = get_base_results_for_ip_analysis_excel(request, subscriber)
    filename = "{}.{}".format("ip_analysis",
                              "xls")
    excel = write_to_excel_ip_analysis(res)
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = u'attachment; filename={}'.format(filename)
    excel.save(response)
    return response

@require_http_methods(["GET"])
@login_required
@get_subscriber_decorator
def view_traffic_analysis(request, subscriber):
    res, show_time, start_date, end_date = get_base_results_for_traffic_analysis(request, subscriber)
    res['traffic_analysis_result'] = get_n_displayble_traffic_details(
        res['traffic_analysis'],
        n=10,
        show_time=show_time,
        timezone=subscriber.timezone,
        start_date=start_date,
        end_date=end_date)

    dates_with_data = set()
    for values in RulesSummary.objects.filter(sid=subscriber, dt__range=[start_date, end_date]).values_list('dt', flat=True):
        dates_with_data.add(values)

    dates_with_data      = [datetime.datetime.strptime(values, '%Y-%m-%d').strftime('%b %d') for values in dates_with_data]
    dates_in_given_range = [dt.strftime('%b %d') for dt in list(rrule.rrule(rrule.DAILY,
                                                                              dtstart=start_date,
                                                                              until=end_date))]
    missing_data_date_range = ta_service.get_missing_data_in_given_date_range(dates_in_given_range,
                                                                              dates_with_data)
    is_data_missing = True if len(missing_data_date_range) else False
    can_edit        = any(is_admin(request.user))
    is_monitor      = is_monitor_mode(subscriber,request.user)
    is_demo_user    = is_demo_user_account(request.user)
    return render(request, 'dashboard.html', {'res'             : res,
                                              'can_edit'        : can_edit,
                                              'is_monitor'      : is_monitor,
                                              'is_demo_user'    : is_demo_user,
                                              'show_time'       : show_time,
                                              'is_data_missing' : is_data_missing})
