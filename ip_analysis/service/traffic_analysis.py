# -*- coding: utf-8 -*-

import json
import datetime
import pytz
from datetime import timedelta
from itertools import product

import arrow

from django.db.models import Sum, Q

from ip_analysis.models import RulesSummary, IpAnalysis


FIELDS = ('genuineusers', 'trustedbots', 'badbots')


def make_datetime_aware_of_timezone(dt, timezone):
    tz = pytz.timezone(timezone)
    return tz.localize(dt)

def is_timezone_ahead_of_utc(tz):
    offset = arrow.now(tz).utcoffset()
    # If offset is 0 timezone is ahead for US/Pacific it will -1
    return offset.days == 0

def convert_timezone(dt, timezone):
    new_dt = arrow.Arrow(dt.year, dt.month, dt.day, getattr(dt, 'hour', 0))
    return new_dt.to(timezone)

def make_minute_from_timezone(hour, timezone):
    tz = pytz.timezone(timezone)
    # Create a datetime object so that we can get offset wrt timezone
    dt = datetime.datetime(2014, 06, 06, hour)
    offset = tz.utcoffset(dt)
    minutes = int(offset.total_seconds() / 60.0 % 60)
    if offset.days < 0:
        if minutes:
            return "%02.f" % (60 - minutes) # If timezone is lagging we need to minus
        else:
            return "%02.f" % minutes
    return "%02.f" % minutes

def _base_for_traffic_analysis(subscriber, start_date, end_date, kwargs):
    timezone = subscriber.timezone
    aware_start_date = make_datetime_aware_of_timezone(
        start_date, timezone) if timezone else start_date
    aware_end_date = make_datetime_aware_of_timezone(
        end_date, timezone) if timezone else end_date

    res = RulesSummary.objects.filter(sid=subscriber, dt__gte=aware_start_date,
                                      dt__lte=aware_end_date).order_by('dt')

    params = {k: Sum(v) for k, v in kwargs.iteritems()}
    aggregated_res = res.aggregate(**params)
    if any(aggregated_res.values()):
        aggregated_res['total'] = sum(aggregated_res.itervalues())
    else:
        aggregated_res['total'] = 0
    return aggregated_res

def _make_rules_summary_item_into_dict(summary, timezone,
                                       hour=None, display_date=False,
                                       start_date=None, end_date=None):
    """Returns RulesSummary model object into displayable dict

    :param summary: Model object
    :param hour: int from 0 to 23
    """
    fields = FIELDS
    # '06 Apr, 21:06 2014'
    dt = summary.dt
    # Very wierd edge case. Some times date object becomes str or unicode
    # This may be problem at source

    if isinstance(dt, basestring):
        dt = datetime.datetime.strptime(summary.dt, "%Y-%m-%d")
        dt = arrow.Arrow(dt.year, dt.month, dt.day, int(hour or 0), tzinfo=pytz.timezone(timezone))

        if (timezone == 'Asia/Kolkata' and hour is None):
            pass
        else:
            dt = dt.to('UTC')

    start_date = arrow.Arrow(start_date.year, start_date.month,
                             start_date.day, start_date.hour,
                             tzinfo=pytz.timezone('UTC'))
    end_date = arrow.Arrow(end_date.year, end_date.month,
                           end_date.day, end_date.hour,
                           tzinfo=pytz.timezone('UTC'))
    # Hack to get correct value for timezone
    end_date += timedelta(hours=24)

    if hour is None:
        name = "{1} {0.day}".format(dt, dt.strftime("%h"))
        summary_dict = {field: getattr(summary, field) for field in fields}
        if start_date.date() <= dt.date() <= end_date.date():
            summary_dict['name'] = name
        else:
            summary_dict['name'] = ""
        return summary_dict

    if display_date:
        name = "{1} {0.day} {2}:00".format(dt, dt.strftime("%h"), hour)
        summary_dict={}
        if start_date.date() <= dt.date() <= end_date.date():
            summary_dict['name'] = name
        else:
            summary_dict['name'] = ""
    else:
        end_date -= timedelta(hours=24)
        if start_date.day <= dt.day <= end_date.day:
            name = "{0}:00".format(dt.hour)
        else:
            name = ""
    summary_dict = {field: getattr(summary, "".join([field, str(hour)]))
                    for field in fields}
    summary_dict['name'] = name

    return summary_dict

def flatten_results(result):
    # converting list to json because python long integers has L at the end
    # Browser interprets them as ILLEGAL Token.
    r = {field: json.dumps([res[field] for res in result]) for field in FIELDS}
    r['names'] = [res['name'] for res in result if 'name' in res]
    return r

def _make_n_items_from_lesser_items(objects, timezone, n, display_date, start_date, end_date):
    index_hours_pair = list(product(range(len(objects)), range(0, 24)))
    picked_items = index_hours_pair
    result = [_make_rules_summary_item_into_dict(objects[item[0]],
                                                 timezone,
                                                 item[1],
                                                 display_date,
                                                 start_date,
                                                 end_date)
            for item in picked_items]
    cleaned_result = [res for res in result if res['name']]
    return cleaned_result

def replace_non_date_fields(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def _get_tz_aware_start_date_and_end_date(subscriber, start_date, end_date):
    offset = arrow.now(subscriber.timezone).utcoffset()
    if offset.seconds == 0:
        # Same or is UTC
        aware_start_date = start_date
        aware_end_date = end_date
    else:
        offset = arrow.now(subscriber.timezone).utcoffset()
        if start_date == end_date:
            if offset.days == 0:
                aware_start_date = start_date
                aware_end_date = end_date
#                 aware_end_date = end_date + timedelta(hours=24)
            else:
                aware_start_date = start_date + timedelta(hours=-24)
                aware_end_date = end_date
        else:
            if offset.days != 0:
                aware_start_date = start_date + timedelta(hours=-24)
                aware_end_date = end_date
            else:
                aware_start_date = start_date
                aware_end_date = end_date + timedelta(hours=24)

    return aware_start_date, aware_end_date

def build_qs_for_traffic_analysis(subscriber, start_date, end_date, max_results=10):
    aware_start_date, aware_end_date = _get_tz_aware_start_date_and_end_date(subscriber,
                                                                             start_date,
                                                                             end_date)
    qs = RulesSummary.objects.filter(sid=subscriber.internal_sid,
                                     dt__lte=aware_end_date,
                                     dt__gte=aware_start_date).order_by('dt')
    return qs

def get_traffic_classification_for_time_range(subscriber, start_date, end_date):
    """Returns dict of genuineusers, trustedbots, badbots and total.

    :param start_date: Python date object
    :param end_date: Python date object
    """
    kwargs = {'genuineusers': 'genuineusers',
              'trustedbots': 'trustedbots',
              'badbots': 'badbots'}
    return _base_for_traffic_analysis(subscriber, start_date, end_date, kwargs)

def get_bad_bot_traffic_for_time_range(subscriber, start_date, end_date):
    kwargs = {'r_browserIntgrity': 'r_browserIntgrity',
              'r_httpRequestIntegrity': 'r_httpRequestIntegrity',
              'r_Aggregator': 'r_Aggregator',
              'r_behaviourIntegrity': 'r_behaviourIntegrity',
              'r_Ratelimiting': 'r_Ratelimiting'}
    return _base_for_traffic_analysis(subscriber, start_date, end_date, kwargs)

def get_bad_bot_actions_for_time_range(subscriber, start_date, end_date):
    kwargs = {'monitor': 'monitor',
              'captcha': 'captcha',
              'block': 'block',
              'feedfakedata': 'feedfakedata'}
    return _base_for_traffic_analysis(subscriber, start_date, end_date, kwargs)

def get_traffic_analysis_for_time_range(subscriber, start_date, end_date=None):
    if not end_date:
        timezone = subscriber.timezone
        aware_start_date = make_datetime_aware_of_timezone(
            start_date, timezone) if timezone else start_date
        return RulesSummary.objects.filter(subscriber,
                                           dt__gte=aware_start_date).order_by('dt')
    return build_qs_for_traffic_analysis(subscriber, start_date, end_date)

def build_qs_for_ip_analysis(subscriber, start_date, end_date, max_results=15.0):
    aware_start_date, aware_end_date =  _get_tz_aware_start_date_and_end_date(subscriber,
                                                                              start_date,
                                                                              end_date)
    return IpAnalysis.objects.filter(sid=subscriber,
                                     dt__lte=aware_end_date,
                                     dt__gte=aware_start_date)

def get_ip_analysis_for_time_range(subscriber, start_date, end_date=None):

    if not end_date:
        return IpAnalysis.objects.filter(subscriber, dt__gte=start_date).all() \
                                                      .values('ipaddress')\
                                                      .annotate(totalrequests         =   Sum('totalrequests'),
                                                                browserIntgrity       =   Sum('browserIntgrity'),
                                                                httpRequestIntegrity  =   Sum('httpRequestIntegrity'),
                                                                Aggregator            =   Sum('Aggregator'),
                                                                behaviourIntegrity    =   Sum('behaviourIntegrity'),
                                                                Ratelimiting          =   Sum('Ratelimiting'),
                                                                genuinerequests       =   Sum('genuinerequests'))\
                                                   .order_by("-totalrequests")
    qs = build_qs_for_ip_analysis(subscriber, start_date, end_date)
#     return qs.filter(~Q(ipaddress__in = white_listed_ips)).order_by("-totalrequests")
    return qs.values('ipaddress')\
                  .annotate(totalrequests         =   Sum('totalrequests'),
                            browserIntgrity       =   Sum('browserIntgrity'),
                            httpRequestIntegrity  =   Sum('httpRequestIntegrity'),
                            Aggregator            =   Sum('Aggregator'),
                            behaviourIntegrity    =   Sum('behaviourIntegrity'),
                            Ratelimiting          =   Sum('Ratelimiting'),
                            genuinerequests       =   Sum('genuinerequests'))\
                  .order_by("-totalrequests")

def get_n_displayble_traffic_details(items, timezone, n, show_time, start_date, end_date):
    if len(items) == n:
        result = [_make_rules_summary_item_into_dict(item, timezone, start_date=start_date, end_date=end_date) for item in items]
        cleaned_result = [res for res in result if res['name']]
        return flatten_results(cleaned_result)
    elif len(items) > n:
        result = [_make_rules_summary_item_into_dict(item, timezone, start_date=start_date, end_date=end_date) for item in items]
        cleaned_result = [res for res in result if res['name']]
        return flatten_results(cleaned_result)
    else:
        if show_time:
            if len(items) >= 3:
                display_date = True
            else:
                display_date = False
            return flatten_results(
                _make_n_items_from_lesser_items(items,
                                                timezone,
                                                n,
                                                display_date,
                                                start_date,
                                                end_date))
        result = [_make_rules_summary_item_into_dict(item, timezone=timezone,
                                                     start_date=start_date,
                                                     end_date=end_date)
                  for item in items]
        cleaned_result = [res for res in result if res['name']]
        return flatten_results(cleaned_result)

def complete_traffic_analysis(subscriber, start_date, end_date):
    traffic_classification = get_traffic_classification_for_time_range(subscriber,
                                                                       start_date,
                                                                       end_date)
    bad_bot_traffic = get_bad_bot_traffic_for_time_range(subscriber,
                                                         start_date,
                                                         end_date)
    bad_bot_actions = get_bad_bot_actions_for_time_range(subscriber,
                                                         start_date,
                                                         end_date)
    traffic_analysis = get_traffic_analysis_for_time_range(subscriber,
                                                           start_date,
                                                           end_date)
    result = {'traffic_classification': traffic_classification,
              'bad_bot_traffic': bad_bot_traffic,
              'bad_bot_actions': bad_bot_actions,
              'traffic_analysis': traffic_analysis}
    return result

def complete_ip_analysis(subscriber, start_date, end_date):
    ip_analysis = get_ip_analysis_for_time_range(subscriber,
                                                 start_date,
                                                 end_date)
    result = {'ip_analysis': ip_analysis, }
    return result

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

def convert_tz_tailored_dates_in_list_to_displayable_date(timezone, dates_list):
    ip_line_graph_date = []
    for items in dates_list:
        converted_date = arrow.Arrow(items.year, items.month, items.day, items.hour, tzinfo=pytz.timezone('UTC'))
        tm = converted_date.format('ZZ')
        converted_hours = int(tm[1:3]) + 1 if int(tm[4:]) > 0 else int(tm[1:3])
        converted_date += timedelta(hours = eval(tm[0] + str(converted_hours)))
        ip_line_graph_date.append(converted_date.format('YYYY-MM-DD HH:mm:ss'))
    return ip_line_graph_date
