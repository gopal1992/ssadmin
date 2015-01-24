from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from aggregator_analysis.excel import write_to_excel_aggregator_ip_analysis
from aggregator_analysis.forms import AggregatorAnalysisSearchForm
from aggregator_analysis.models import AggregatorDetails
from aggregator_analysis.service import get_base_results_for_aggregator_analysis_excel, \
    get_aggregator_analysis_details
from ip_analysis.service.ip_analysis_details import convert_date_specific_to_timezone
from ip_analysis.views import _get_date_from_timestamp
from service_layer.page_authorization import get_authorized_pages
from utils.account import get_subscriber_decorator, is_normal_user, is_admin, \
    is_monitor_mode, is_demo_user_account


@require_http_methods(["GET"])
@login_required
@user_passes_test(is_normal_user)
@get_subscriber_decorator
def excel_view_aggregator_analysis(request, subscriber):
    """
    This Function is defined to carry out excel download of the data(s) being retrieved for Aggregator IP Analysis.
    """
    # Changing any key will affect in multiple places.
    result_for_excel_sheet  = get_base_results_for_aggregator_analysis_excel(request, subscriber)
    filename    = "{}.{}".format("aggregator_ip_analysis", "xls")
    excel       = write_to_excel_aggregator_ip_analysis(result_for_excel_sheet)
    response    = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = u'attachment; filename={}'.format(filename)
    excel.save(response)
    return response

@require_http_methods(["GET"])
@login_required
@get_subscriber_decorator
def list_aggregator_analysis_details(request, subscriber):
    """
    This Function is responsible to provide Aggregator list details for the landing page of Aggregator IP Analysis
    """
    page_no = request.GET.get('page', 1)

    start_date_utc  = request.GET.get('date_from')
    end_date_utc    = request.GET.get('date_to')

    start_date, end_date = _get_date_from_timestamp(request, start_date_utc, end_date_utc)
    form = AggregatorAnalysisSearchForm(request.GET)

    search_ip_address       = None
    search_aggregator_name  = None

    if form.is_valid():
        search_ip_address       = form.cleaned_data['ip_address'].strip()
        search_aggregator_name  = form.cleaned_data['aggregator_name'].strip()

    start_date, end_date = convert_date_specific_to_timezone(subscriber.timezone, start_date, end_date)

    # Call service layer to fetch the details
    data = get_aggregator_analysis_details(subscriber,
                                           search_ip_address,
                                           search_aggregator_name,
                                           start_date,
                                           end_date)

    paginator = Paginator(data, 15)
    aggregator_analysis_details = None
    try:
        aggregator_analysis_details = paginator.page(page_no)
    except PageNotAnInteger:
        aggregator_analysis_details = paginator.page(page_no)
    except EmptyPage:
        aggregator_analysis_details = paginator.page(paginator.num_pages)

    aggregator_analysis_details_table = [] # List of dicts for HTML rendering
    for aggregator_analysis_detail in aggregator_analysis_details:
        ip_address = AggregatorDetails.objects.get(pk = aggregator_analysis_detail['ip_address'])
        aggregator_analysis_details_dict = {'id'                :   0,
                                            'ip_address'        :   ip_address.ip_address,
                                            'aggregator_name'   :   ip_address.aggregator_name,
                                            'bot_hits'          :   aggregator_analysis_detail['total_requests']}

        aggregator_analysis_details_table.append(aggregator_analysis_details_dict)

    search = False
    if any([search_ip_address, search_aggregator_name]):
        search = True

    can_edit        = any(is_admin(request.user))
    is_monitor      = is_monitor_mode(subscriber,request.user)
    is_demo_user    = is_demo_user_account(request.user)
    authorized_page_list = get_authorized_pages(subscriber)
    return render(request,
                  'aggregator_analysis.html',
                  {'search_from'                      : form,
                   'aggregator_analysis_details'      : aggregator_analysis_details,
                   'aggregator_analysis_details_table': aggregator_analysis_details_table,
                   'can_edit'                         : can_edit,
                   'is_demo_user'                     : is_demo_user,
                   'is_monitor'                       : is_monitor,
                   'search'                           : search,
                   'auth_pages'                       : authorized_page_list
                  })
