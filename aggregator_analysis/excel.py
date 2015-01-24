import xlwt

from aggregator_analysis.models import AggregatorDetails


def write_to_excel_aggregator_ip_analysis(data):
    """
    @param data: dict of all worksheet data
    """
    #:TODO: Refactor code into smaller functions

    wb = xlwt.Workbook(encoding='utf-8')
    # Don't try to refactor this code into generic one.
    # You will regret later.
    # Being specific is easier here
    ws = wb.add_sheet("Aggregator IP Analysis")

    # We need to need traffic_analysis key
    summary_data = data.get('aggregator_ip_analysis')
    row_num = 0

    # First column is legend because we need to display date
    columns = ['Aggregator', 'IP Address', 'Total Requests']

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num, column_heading in enumerate(columns):
        ws.write(row_num, col_num, column_heading, font_style)

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 0

    data_to_inject = []
    for ip_analysis_detail in summary_data:
        ipaddress = AggregatorDetails.objects.get(pk = ip_analysis_detail['ip_address'])
        data_to_inject.append([ipaddress.aggregator_name,
                               ipaddress.ip_address,
                               ip_analysis_detail['total_requests'],
                               ])

    for obj in data_to_inject:
        row_num += 1
        row = obj
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    return wb