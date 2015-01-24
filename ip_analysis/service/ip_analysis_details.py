# -*- coding: utf-8 -*-
from datetime import timedelta
import datetime
import json

import arrow
from django.db.models import Q, Sum
import pytz

from ip_analysis.forms import IpActionForm
from ip_analysis.models import IpAnalysis, IpActions, IpDetails, IpStatus, \
    ResponseCode
from ssadmin.base_settings import HOURLY_DATE


def update_ip_action(subscriber, action, expiry_date, ip_address):
    ipdetails = IpDetails.objects.filter(ip_address=ip_address)
    ipactions = IpActions.objects.filter(sid=subscriber.pk, ip_address=ipdetails[0].id)
    response  = ResponseCode.objects.filter(id = action)
    if not ipactions:
        ipstatus  = IpStatus.objects.filter(id = 0)
        ipactions = IpActions.objects.create(sid = subscriber,
                                             ip_address  = ipdetails[0],
                                             action = response[0],
                                             expiry_date = expiry_date,
                                             status = ipstatus[0] )
        ipactions.save()
        return ipactions.action.response, ipactions.expiry_date.strftime('%b. %d, %Y')
    ipactions[0].action  = response[0]
    ipactions[0].expiry_date = expiry_date
    ipactions[0].save()
    return ipactions[0].action.response, (ipactions[0].expiry_date).strftime('%b. %d, %Y')

def convert_date_specific_to_timezone(timezone, start_date, end_date):
    '''
    USE CASE: Date is converted to timezone specific.

    :param start_date = datetime object
    :param end_date = datetime object

    The start_date is taken as reference for converting to timezone specific dates.
    start_date is converted to UTC then to subscriber timezone specific.
    Now the converted date is utilized to fetch the hour difference w.r.t UTC.(i.e. +05.30, -11.30)
    start_date is reduced by "-XX:YY" if the tm is "+XX:YY" and vice versa, same for end_date as well.
    At last the end_date is incremented by a day for fetching data in the mentioned date range.
    '''
    date_to_utc     =   arrow.Arrow(start_date.year, start_date.month,
                                    start_date.day, start_date.hour,
                                    tzinfo=pytz.timezone('UTC'))
    converted_date  =   arrow.Arrow(date_to_utc.year, date_to_utc.month,
                                    date_to_utc.day, date_to_utc.hour,
                                    tzinfo=pytz.timezone(timezone))
    tm = converted_date.format('ZZ')
    converted_hours = int(tm[1:3]) + 1 if int(tm[4:]) > 0 else int(tm[1:3])
    start_date     -= timedelta(hours = eval(tm[0] + str(converted_hours)))
    end_date       -= timedelta(hours = eval(tm[0] + str(converted_hours)))
    end_date       += timedelta(hours = 23)
    return start_date, end_date

def convert_tz_tailored_dates_in_list_to_displayable_date(timezone, dates_list):
    ip_line_graph_date = []
    for item in dates_list:
        item = datetime.datetime.strptime(str(item.split(".")[0]), '%Y-%m-%d %H:%M:%S')
        converted_date = arrow.Arrow(item.year, item.month, item.day, item.hour, tzinfo=pytz.timezone(timezone))
        tm = converted_date.format('ZZ')
        converted_hours = int(tm[1:3]) + 1 if int(tm[4:]) > 0 else int(tm[1:3])
        converted_date += timedelta(hours = eval(tm[0] + str(converted_hours)))
        ip_line_graph_date.append(converted_date.format('YYYY-MM-DD HH:mm:ss'))

    return ip_line_graph_date

def hourly_date_available_message_display(start_date):
#     start_date  = datetime.datetime.strptime(start_date.split(' ')[0], "%Y-%m-%d")
    hourly_date = datetime.datetime.strptime(HOURLY_DATE, "%Y-%m-%d")
    displayable_date = datetime.datetime.strptime(HOURLY_DATE, "%Y-%m-%d").strftime("%B %d, %Y")
    return displayable_date if start_date < hourly_date else ''

def convert_datetime_to_hours_or_date(list_of_dates, show_time):
    list_of_dates = [datetime.datetime.strptime(str(x.split(".")[0]), '%Y-%m-%d %H:%M:%S') for x in list_of_dates]
    if show_time:
        list_of_dates = [x.strftime('%Y-%m-%d %H:%M:%S') for x in list_of_dates]
        list_of_dates = sorted(list(set(list_of_dates)), key=lambda x: x)
        set_list_dates = [datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').strftime('%b %d, %H:%M') for x in list_of_dates]
    else:
        list_of_dates = [x.strftime('%Y-%m-%d') for x in list_of_dates]
        list_of_dates = sorted(list(set(list_of_dates)), key=lambda x: x)
        set_list_dates = [datetime.datetime.strptime(str(x), '%Y-%m-%d').strftime('%b %d') for x in list_of_dates]
    return set_list_dates

def optimize_data_based_on_number_of_days(list_of_dates, list_of_values, show_time):
    new_list_of_date  = []
    new_list_of_value = []
    converted_dates = convert_datetime_to_hours_or_date(list_of_dates, show_time)
    if not show_time:
        for i in converted_dates:
            new_list_of_date.append(i)
            temp = 0
            for v,j in enumerate(list_of_dates):
                if i == datetime.datetime.strptime(str(j.split(".")[0]), '%Y-%m-%d %H:%M:%S').strftime('%b %d'):
                    temp += int(list_of_values[v])
            new_list_of_value.append(temp)
        list_of_values = new_list_of_value

    return converted_dates, list_of_values

def get_ip_actions_for_given_ip_address(subscriber, ip_address):
    ip_action_form = IpActionForm()
    ip_action_instance = IpActions.objects.filter(sid = subscriber, ip_address = ip_address)
    if ip_action_instance:
        ip_action_form.fields['action'].initial = ip_action_instance[0].action.id
        ip_action_form.fields['expiry_date'].initial = datetime.datetime.strptime(str((ip_action_instance[0].expiry_date)), "%Y-%m-%d").strftime('%b. %d, %Y')
        ip_action = ip_action_instance[0].action
        expiry_date = datetime.datetime.strptime(str((ip_action_instance[0].expiry_date)), "%Y-%m-%d").strftime('%Y-%m-%d')
    else:
        ip_action_form.fields['action'].initial = 0
        ip_action_form.fields['expiry_date'].initial = ''
        ip_action  = ''
        expiry_date = (datetime.date.today() + timedelta(days = 7)).strftime('%Y-%m-%d')
    return ip_action_form, ip_action, expiry_date

def individual_ip_address_details(subscriber, ip_address, start_date, end_date, show_time):
    ip_line_graph_date = [] # Name of list to represent X axis for the Line graph in Detailed IP information
    ip_line_graph_hits = [] # Name of list to represent Y axis for the Line graph in Detailed IP information

    line_graph_ip_object = IpAnalysis.objects.filter(sid = subscriber,
                                                     ipaddress = ip_address,
                                                     dt__range = [start_date, end_date])
    ip_action_form, ip_action, expiry_date = get_ip_actions_for_given_ip_address(subscriber, ip_address)
    for ips in line_graph_ip_object:
        conv_date       = str(ips.dt)
        totalrequests   = json.dumps(ips.totalrequests)
        ip_line_graph_date.append(conv_date)
        ip_line_graph_hits.append(totalrequests)

    hourly_message = hourly_date_available_message_display(start_date)

    ip_line_graph_date = convert_tz_tailored_dates_in_list_to_displayable_date(subscriber.timezone, ip_line_graph_date)
    ip_line_graph_date, ip_line_graph_hits = optimize_data_based_on_number_of_days(ip_line_graph_date, ip_line_graph_hits, show_time)

    return ip_action_form, ip_line_graph_date, json.dumps(ip_line_graph_hits), ip_action, expiry_date, hourly_message

def get_ip_analysis_details(subscriber,
                            ip_address,
                            country_name,
                            isp,
                            city_name,
                            status,
                            date_from,
                            date_to):

    # Filter from the IpAddressAccessList table for SID, ip_address & access_status
    ip_analysis_query = IpAnalysis.objects.all() \
                                          .values('ipaddress')\
                                          .annotate(totalrequests         =   Sum('totalrequests'),
                                                    browserIntgrity       =   Sum('browserIntgrity'),
                                                    httpRequestIntegrity  =   Sum('httpRequestIntegrity'),
                                                    Aggregator            =   Sum('Aggregator'),
                                                    behaviourIntegrity    =   Sum('behaviourIntegrity'),
                                                    Ratelimiting          =   Sum('Ratelimiting'),
                                                    genuinerequests       =   Sum('genuinerequests'))\
                                          .order_by("-totalrequests")

    query = Q(sid=subscriber) & Q(dt__range=[date_from, date_to])

    if ip_address:
        query = query & Q(ipaddress__ip_address__icontains=ip_address)
        return ip_analysis_query.filter(query)

    if isp:
        query = query & Q(ipaddress__isp__icontains=isp)
        return ip_analysis_query.filter(query)

    if country_name:
        query = query & Q(ipaddress__country_name__icontains=country_name)
        return ip_analysis_query.filter(query)

    if city_name:
        query = query & Q(ipaddress__city_name__icontains=city_name)
        return ip_analysis_query.filter(query)

    if status:
        malicious_ips   =   IpActions.objects.filter(sid = subscriber, status = IpStatus.objects.filter(id=1)[0].id).values('ip_address')
        if status.lower() == "clean":
            query = query & ~Q(ipaddress = malicious_ips)
            ip_anlaysis_query = ip_analysis_query.filter(query)
        elif status.lower() == "malicious":
            query = query & Q(ipaddress = malicious_ips)
            ip_anlaysis_query = ip_analysis_query.filter(query)
        else:
            ip_anlaysis_query = []
        return ip_anlaysis_query

    # Return all the records for the subscriber
    return ip_analysis_query.filter(query)