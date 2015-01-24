from datetime import timedelta
import datetime
import json

import arrow
from dateutil import rrule
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.aggregates import Sum
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import pytz

from data_migration.models import NewRulesSummary
from ip_analysis.service.excel import write_to_excel_traffic_analysis
from ip_analysis.views import DELAY_DAYS
from service_layer.page_authorization import get_authorized_pages
from utils.account import get_subscriber_decorator, is_admin, is_monitor_mode, \
    is_demo_user_account, is_normal_user


def get_missing_data_in_given_date_range(dates_in_given_range, dates_with_data):
    """
    Use Case: Fetch the dates during which the data is missing

    :param dates_in_given_range = List of dates present is the date range selected by the user
    :param dates_with_data = List of dates where data is collected between the date range selected by the user

    The dates_with_data is set() functioned to obtain the distinct dates in the specified date range.
    Then the dates which does not have data in the specified data range is found by performing difference_update()
    function and the list of values is returned.
    """
    missing_data_date_range = set(dates_in_given_range)
    missing_data_date_range.difference_update(dates_with_data)
    return list(missing_data_date_range)

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
    end_date       += timedelta(hours=23)
    return start_date, end_date

def convert_tz_tailored_dates_in_list_to_displayable_date(timezone, dates_list):
    ip_line_graph_date = []
    for items in dates_list:
        converted_date = arrow.Arrow(items.year, items.month, items.day, items.hour, tzinfo=pytz.timezone(timezone))
        tm = converted_date.format('ZZ')
        converted_hours = int(tm[1:3]) + 1 if int(tm[4:]) > 0 else int(tm[1:3])
        converted_date += timedelta(hours = eval(tm[0] + str(converted_hours)))
        ip_line_graph_date.append(converted_date.format('YYYY-MM-DD HH:mm:ss'))

    return ip_line_graph_date

def get_reverse_timezone_converted_dates(dates_list, timezone):
    ip_line_graph_date = []
    for items in dates_list:
        items   =   datetime.datetime.strptime(str(items), '%Y-%m-%d %H:%M:%S')
        converted_date = arrow.Arrow(items.year, items.month, items.day, items.hour, tzinfo=pytz.timezone(timezone))
        tm = converted_date.format('ZZ')
        converted_hours = int(tm[1:3]) + 1 if int(tm[4:]) > 0 else int(tm[1:3])
        converted_date += timedelta(hours = eval(tm[0] + str(converted_hours)))
        ip_line_graph_date.append(converted_date.format('YYYY-MM-DD HH:mm:ss'))

    return ip_line_graph_date

def optimize_data_based_on_number_of_days(list_of_dates, converted_dates, list_of_values, show_time):
    new_list_of_date  = []
    new_list_of_value = []
    if not show_time:
        for i in list_of_dates:
            new_list_of_date.append(i)
            temp = 0
            for v,j in enumerate(converted_dates):
                if i == datetime.datetime.strptime(str(j), '%Y-%m-%d %H:%M:%S').strftime('%b %d'):
                    temp += int(list_of_values[v])
            new_list_of_value.append(temp)
        list_of_values = new_list_of_value

    return list_of_dates, list_of_values

def convert_datetime_to_hours_or_date(list_of_dates, show_time, timezone):
    list_of_dates = [datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S') for x in list_of_dates]
    if show_time:
        list_of_dates = [x.strftime('%Y-%m-%d %H:%M:%S') for x in list_of_dates]
        list_of_dates = sorted(list(set(list_of_dates)), key=lambda x: x)
        list_of_dates = get_reverse_timezone_converted_dates(list_of_dates, timezone)
        set_list_dates = [datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').strftime('%b %d, %H:%M') for x in list_of_dates]
    else:
        list_of_dates = [x.strftime('%Y-%m-%d') for x in list_of_dates]
        list_of_dates = sorted(list(set(list_of_dates)), key=lambda x: x)
        set_list_dates = [datetime.datetime.strptime(str(x), '%Y-%m-%d').strftime('%b %d') for x in list_of_dates]
    return set_list_dates

def complete_traffic_analysis(subscriber, start_date, end_date):
    query = Q(sid=subscriber.pk, dt__range=[start_date, end_date])
    items = NewRulesSummary.objects.filter(query).order_by('dt')
    traffic_classification = NewRulesSummary.objects.filter(query)\
                             .order_by('dt').aggregate(trustedbots = Sum('trusted_bots'),
                              genuineusers = Sum('genuine_users'),
                              r_Aggregator = Sum('r_aggregator'),
                              badbots = Sum('bad_bots'),
                              total = Sum('all_api'))
    bad_bot_traffic = NewRulesSummary.objects.filter(query)\
                              .order_by('dt').aggregate(r_browserIntgrity = Sum('r_browser_integrity'),
                              r_httpRequestIntegrity = Sum('r_http_request_integrity'),
                              r_Aggregator = Sum('r_aggregator'),
                              r_behaviourIntegrity = Sum('r_behaviour_integrity'),
                              r_Ratelimiting = Sum('r_rate_limiting'))
    bad_bot_actions = NewRulesSummary.objects.filter(query)\
                              .order_by('dt').aggregate(monitor = Sum('monitor'),
                              captcha = Sum('captcha'),
                              block   = Sum('block'),
                              feedfakedata = Sum('feed_fake_data'))
    bad_bot_traffic['total'] = sum([int(i) if i != None else int(0) for i in bad_bot_traffic.values()])
    bad_bot_actions['total'] = sum([int(i) if i != None else int(0) for i in bad_bot_actions.values()])
    traffic_analysis = [item for item in items]
    result = {'traffic_classification'  : traffic_classification,
              'bad_bot_traffic'         : bad_bot_traffic,
              'bad_bot_actions'         : bad_bot_actions,
              'traffic_analysis'        : traffic_analysis}
    return result

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

def get_n_displayble_traffic_details(result, timezone, show_time, start_date, end_date):
    list_of_dates           = [items.dt for items in result]
    list_of_bad_bots        = [items.bad_bots for items in result]
    list_of_trusted_bots    = [items.trusted_bots for items in result]
    list_of_aggregator      = [items.r_aggregator for items in result]
    list_of_genuine_users   = [items.genuine_users for items in result]
    if len(list(set([item.strftime('%Y-%m-%d') for item in list_of_dates]))) <= 3:
        show_time = True

    converted_dates         = convert_tz_tailored_dates_in_list_to_displayable_date(timezone, list_of_dates)
    list_of_dates           = convert_datetime_to_hours_or_date(list_of_dates, show_time, timezone)

    if not show_time:
        list_of_dates, list_of_bad_bots     = optimize_data_based_on_number_of_days(list_of_dates, converted_dates, list_of_bad_bots, show_time)
        list_of_dates, list_of_trusted_bots = optimize_data_based_on_number_of_days(list_of_dates, converted_dates, list_of_trusted_bots, show_time)
        list_of_dates, list_of_aggregator   = optimize_data_based_on_number_of_days(list_of_dates, converted_dates, list_of_aggregator, show_time)
        list_of_dates, list_of_genuine_users= optimize_data_based_on_number_of_days(list_of_dates, converted_dates, list_of_genuine_users, show_time)

    result = {'trustedbots' : json.dumps(list_of_trusted_bots),
              'genuineusers': json.dumps(list_of_genuine_users),
              'aggregator'  : json.dumps(list_of_aggregator),
              'badbots'     : json.dumps(list_of_bad_bots),
              'names'       : list_of_dates}

    return result

def get_base_results_for_traffic_analysis(request, subscriber):
    start_date_utc  = request.GET.get('start_date')
    end_date_utc    = request.GET.get('end_date')

    actual_start_date, actual_end_date = _get_date_from_timestamp(request, start_date_utc, end_date_utc)
    start_date, end_date = convert_date_specific_to_timezone(subscriber.timezone, actual_start_date, actual_end_date)

    diff        = end_date - start_date
    show_time   = True if diff.days < 3 else False
    return complete_traffic_analysis(subscriber, start_date, end_date), show_time, start_date, end_date, actual_start_date, actual_end_date

@require_http_methods(["GET"])
@login_required
@user_passes_test(is_normal_user)
@get_subscriber_decorator
def excel_view_traffic_analysis(request, subscriber):
    res, show_time, start_date, end_date, actual_start_date, actual_end_date = get_base_results_for_traffic_analysis(request, subscriber)
    res['traffic_analysis_result'] = get_n_displayble_traffic_details(res['traffic_analysis'],
                                                                      timezone = subscriber.timezone,
                                                                      show_time=show_time,
                                                                      start_date=start_date,
                                                                      end_date=end_date)
    filename        = "{}.{}".format("traffic_analysis",
                              "xls")
    is_monitor      = is_monitor_mode(subscriber,request.user)
    excel           = write_to_excel_traffic_analysis(res,show_time, is_monitor)
    response        = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = u'attachment; filename={}'.format(filename)
    excel.save(response)
    return response

@require_http_methods(["GET"])
@login_required
@get_subscriber_decorator
def new_view_traffic_analysis(request, subscriber):
    res, show_time, start_date, end_date, actual_start_date, actual_end_date = get_base_results_for_traffic_analysis(request, subscriber)
    res['traffic_analysis_result'] = get_n_displayble_traffic_details(
        res['traffic_analysis'],
        timezone = subscriber.timezone,
        show_time=show_time,
        start_date=start_date,
        end_date=end_date)
    dates_with_data = set()
    for values in NewRulesSummary.objects.filter(sid=subscriber, dt__range=[start_date, end_date])\
                 .values_list('dt', flat=True):
        dates_with_data.add(values)

    if show_time:
        dates_with_data      = [values.strftime('%b %d, %H:%M') for values in dates_with_data]
        dates_in_given_range = [dt.strftime('%b %d, %H:%M') for dt in list(rrule.rrule(rrule.HOURLY,
                                                                                dtstart=start_date,
                                                                                until=end_date))]
    else:
        dates_with_data      = [values.strftime('%b %d') for values in dates_with_data]
        dates_in_given_range = [dt.strftime('%b %d') for dt in list(rrule.rrule(rrule.DAILY,
                                                                                dtstart=start_date,
                                                                                until=end_date))]
    missing_data_date_range = get_missing_data_in_given_date_range(dates_in_given_range, dates_with_data)
    is_data_missing = True if len(missing_data_date_range) else False

    can_edit        = any(is_admin(request.user))
    is_monitor      = is_monitor_mode(subscriber,request.user)
    is_demo_user    = is_demo_user_account(request.user)
    authorized_page_list = get_authorized_pages(subscriber)
    return render(request, 'dashboard.html', {'res'             : res,
                                              'can_edit'        : can_edit,
                                              'is_monitor'      : is_monitor,
                                              'is_demo_user'    : is_demo_user,
                                              'auth_pages'      : authorized_page_list,
                                              'show_time'       : show_time,
                                              'is_data_missing' : is_data_missing,
                                              })

