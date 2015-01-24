# -*- coding: utf-8 -*-

import json

import xlwt

from ip_analysis.models import IpDetails


def write_to_excel_traffic_analysis(data, show_time, is_monitor):
    """
    @param data: dict of all worksheet data
    """
    #:TODO: Refactor code into smaller functions

    wb = xlwt.Workbook(encoding='utf-8')
    # First write traffic summary
    # Don't try to refactor this code into genric one.
    # You will regret later.
    # Being specific is easier here
    ws = wb.add_sheet("traffic_summary")

    # We need to need traffic_analysis key
    data.pop('traffic_analysis', [])
    summary_data = data.get('traffic_analysis_result')
    row_num = 0

    # First column is legend because we need to display date
    if show_time:
        columns = ['Date & Time', 'Genuine Users', 'Crawlers', 'Aggregators', 'Bad Bots']
    else:
        columns = ['Date', 'Genuine Users', 'Crawlers', 'Aggregators', 'Bad Bots']

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num, column_heading in enumerate(columns):
        ws.write(row_num, col_num, column_heading, font_style)

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    # because we did json.loads for template view, doing reverse
    dates         = summary_data.get('names')
    genuine_users = json.loads(summary_data.get('genuineusers'))
    trusted_bots  = json.loads(summary_data.get('trustedbots'))
    aggregator    = json.loads(summary_data.get('aggregator'))
    badbots       = json.loads(summary_data.get('badbots'))

    data_to_inject = zip(dates, genuine_users, trusted_bots, aggregator, badbots)

    for obj in data_to_inject:
        row_num += 1
        row = obj
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    # Traffic classification
    ws = wb.add_sheet("traffic_classification")
    classfication_data = data.get('traffic_classification')
    total = classfication_data.pop('total')

    #We need to put total at the end
    columns = ['Crawlers', 'Genuine Users', 'Aggregators', 'Bad Bots']
    columns.append('Total')

    rows = classfication_data.values()
    #Append total value
    rows.append(total)

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    row_num = 0
    for col_num, column_heading in enumerate(columns):
        # or operation to convert None to 0
        val = column_heading or 0
        ws.write(row_num, col_num, val, font_style)

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    row_num += 1

    for index, item in enumerate(rows):
        ws.write(row_num, index, item or 0, font_style)

    # Bad Bot Traffic
    # Map database field to names in spec
    # if db field is changed this will stop working
    name_mapper = {
        'r_behaviourIntegrity'  : 'Behaviour Integrity Check Failed',
        'r_browserIntgrity'     : 'Browser Integrity Check Failed',
        'r_Ratelimiting'        : 'Rate Limiting Threshold Exceeded',
        'r_httpRequestIntegrity': 'HTTP Request Integrity Check Failed',
        'r_Aggregator'          : 'Aggregator Bot Traffic'
    }

    ws = wb.add_sheet("bad_bot_traffic")
    bad_bot_traffic = data.get('bad_bot_traffic')
    total = bad_bot_traffic.pop('total', 0)

    columns = bad_bot_traffic.keys()
    columns.append("Total")

    rows = bad_bot_traffic.values()
    rows.append(total)

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    row_num = 0
    for col_num, column_heading in enumerate(columns):
        if column_heading != "Total":
            val = name_mapper[column_heading]
        else:
            val = "Total"
        ws.write(row_num, col_num, val, font_style)

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    row_num += 1

    for index, item in enumerate(rows):
        # or'ing to avoid empty string
        ws.write(row_num, index, item or 0, font_style)

    if not is_monitor:
        # Analysis of bad bot traffic
        ws = wb.add_sheet("bad_bot_actions")
        bad_bot_actions = data.get('bad_bot_actions')

        total = bad_bot_actions.pop('total', 0)

        # columns = bad_bot_actions.keys()
        columns = ['Captcha', 'Feed Fake Data', 'Allow', 'Block']
        columns.append("Total")

        rows = bad_bot_actions.values()
        rows.append(total)

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        row_num = 0
        for col_num, column_heading in enumerate(columns):
            ws.write(row_num, col_num, column_heading, font_style)

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        row_num += 1

        for index, item in enumerate(rows):
            ws.write(row_num, index, item or 0, font_style)

    # raise
    return wb

def write_to_excel_ip_analysis(data):
    """
    @param data: dict of all worksheet data
    """
    #:TODO: Refactor code into smaller functions

    wb = xlwt.Workbook(encoding='utf-8')
    # First write traffic summary
    # Don't try to refactor this code into generic one.
    # You will regret later.
    # Being specific is easier here
    ws = wb.add_sheet("IP Analysis")

    # We need to need traffic_analysis key
    summary_data = data.get('ip_analysis')
    row_num = 0

    # First column is legend because we need to display date
    columns = ['IP Address', 'ISP', 'City', 'Country',
               'Total Requests',
               'Browser Integrity Check Failed',
               'Rate Limiting Threshold Check Failed',
               'HTTP Request Integrity Check Failed',
               'Behaviour Integrity Check Failed']

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num, column_heading in enumerate(columns):
        ws.write(row_num, col_num, column_heading, font_style)

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 0

    data_to_inject = []
    for ip_analysis_detail in summary_data:
        ipaddress = IpDetails.objects.get(pk = ip_analysis_detail['ipaddress'])
        data_to_inject.append([ipaddress.ip_address,
                               ipaddress.isp,
                               ipaddress.city_name,
                               ipaddress.country_name,
                               ip_analysis_detail['totalrequests'],
                               ip_analysis_detail['browserIntgrity'],
                               ip_analysis_detail['Ratelimiting'],
                               ip_analysis_detail['httpRequestIntegrity'],
                               ip_analysis_detail['behaviourIntegrity']
                               ])

    for obj in data_to_inject:
        row_num += 1
        row = obj
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    return wb
