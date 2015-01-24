from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.aggregates import Sum
from django.db.models.query_utils import Q
import xlwt

from ip_analysis.service.ip_analysis_details import convert_date_specific_to_timezone
from persistance.user_analysis import UserAnalysis
from utils.datetime_utils import _get_date_from_timestamp


def get_base_results_for_user_analysis_excel(request, subscriber):
    start_date_utc       = request.GET.get('date_from')
    end_date_utc         = request.GET.get('date_to')
    start_date, end_date = _get_date_from_timestamp(request, start_date_utc, end_date_utc)

    search_user_id       = None

    start_date, end_date = convert_date_specific_to_timezone(subscriber.timezone, start_date, end_date)
    user_analysis_data, query   = get_user_analysis_details(subscriber,
                                                            search_user_id,
                                                            start_date,
                                                            end_date)
    x, y, paginator = pagination_for_user_analysis_page(user_analysis_data, query, 1)#x, y parameters are dummy and not intented to use anywhere
    paginator = flattening_results_of_paginated_objects(paginator.object_list, query)
    result = {'user_ip_analysis': paginator, }
    return result

def write_to_excel_user_analysis(data):
    #:TODO: Refactor code into smaller functions

    wb = xlwt.Workbook(encoding='utf-8')
    # Don't try to refactor this code into generic one.
    # You will regret later.
    # Being specific is easier here
    ws = wb.add_sheet("User Analysis")

    # We need to need traffic_analysis key
    summary_data = data.get('user_ip_analysis')
    row_num = 0

    # First column is legend because we need to display date
    columns = ['User ID', 'No.of Distinct bot IPs', 'Total Requests']

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num, column_heading in enumerate(columns):
        ws.write(row_num, col_num, column_heading, font_style)

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 0

    data_to_inject = []
    for data in summary_data:
        try:
            data['user_id'] = int(data['user_id'])
        except ValueError:
            pass
        data_to_inject.append([data['user_id'], data['no_of_distinct_ips'], data['total_requests']])

    for obj in data_to_inject:
        row_num += 1
        row = obj
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    return wb

def get_user_analysis_details(subscriber, user_id, start_date, end_date):
    user_analysis_query = UserAnalysis.objects.filter(sid=subscriber, dt__range=[start_date, end_date])\
                                                    .values('user_id')\
                                                    .annotate(total_requests = Sum('total_requests'))\
                                                    .order_by("-total_requests")

    query = Q(sid=subscriber) & Q(dt__range=[start_date, end_date])
    if user_id:
        return user_analysis_query.filter(user_id__icontains=user_id), query

    return user_analysis_query, query

def flattening_results_of_paginated_objects(user_analysis_query, query):
    list_of_dict = []
    for i in user_analysis_query:
        final_dict = {}
        qs = query & Q(user_id = i['user_id'])
        final_dict['user_id'] = i['user_id']
        final_dict['no_of_distinct_ips'] = UserAnalysis.objects.filter(qs).values_list('ip_address').distinct().count()
        final_dict['total_requests'] = i['total_requests']
        list_of_dict.append(final_dict)
    return list_of_dict

def pagination_for_user_analysis_page(user_analysis_objects, query, page_no):
    per_page = 15
    paginator = Paginator(user_analysis_objects, per_page)
    user_analysis_details = None
    try:
        user_analysis_details = paginator.page(page_no)
    except PageNotAnInteger:
        user_analysis_details = paginator.page(page_no)
    except EmptyPage:
        user_analysis_details = paginator.page(paginator.num_pages)

    user_analysis_details_table = [] # List of dicts for HTML rendering
    user_analysis_details_paginated = flattening_results_of_paginated_objects(user_analysis_details, query)

    for detail in user_analysis_details_paginated:
        user_analysis_details_table.append({'user_id'              :   detail['user_id'],
                                            'no_of_distinct_ips'   :   detail['no_of_distinct_ips'],
                                            'no_of_hits'           :   detail['total_requests'],
                                            })

    return user_analysis_details_table, user_analysis_details, paginator