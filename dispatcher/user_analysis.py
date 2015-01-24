from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from form_layer.user_analysis import UserAnalysisSearchForm
from ip_analysis.service.ip_analysis_details import convert_date_specific_to_timezone
from ip_analysis.views import _get_date_from_timestamp
from service_layer.page_authorization import get_authorized_pages
from service_layer.user_analysis import get_user_analysis_details, \
    get_base_results_for_user_analysis_excel, write_to_excel_user_analysis, \
    pagination_for_user_analysis_page
from utils.account import get_subscriber_decorator, is_admin, is_monitor_mode, \
     is_demo_user_account, is_normal_user
from utils.decorator import access_to_page


@require_http_methods(["GET"])
@login_required
@user_passes_test(is_normal_user)
@get_subscriber_decorator
def excel_view_user_analysis(request, subscriber):
    result_for_excel_sheet  = get_base_results_for_user_analysis_excel(request, subscriber)
    filename                = "{}.{}".format("user_analysis","xls")
    excel                   = write_to_excel_user_analysis(result_for_excel_sheet)
    response                = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = u'attachment; filename={}'.format(filename)
    excel.save(response)
    return response

@require_http_methods(["GET"])
@login_required
@get_subscriber_decorator
@access_to_page('User Analysis')
def list_user_analysis_details(request, subscriber):
    page_no = request.GET.get('page', 1)

    start_date_utc  = request.GET.get('date_from')
    end_date_utc    = request.GET.get('date_to')

    start_date, end_date = _get_date_from_timestamp(request, start_date_utc, end_date_utc)
    form = UserAnalysisSearchForm(request.GET)

    search_user_id   = None

    if form.is_valid():
        search_user_id   = form.cleaned_data['user_id'].strip()

    start_date, end_date = convert_date_specific_to_timezone(subscriber.timezone, start_date, end_date)

    # Call service layer to fetch the details
    data, query = get_user_analysis_details(subscriber, search_user_id, start_date, end_date)

    user_analysis_details_table, user_analysis_details, z  = pagination_for_user_analysis_page(data, query, page_no)

    search = False
    if any([search_user_id]):
        search = True

    can_edit                = any(is_admin(request.user))
    is_monitor              = is_monitor_mode(subscriber,request.user)
    is_demo_user            = is_demo_user_account(request.user)
    authorized_page_list    = get_authorized_pages(subscriber)

    return render(request,
                  'user_analysis.html',
                  {'user_analysis_details_table'    : user_analysis_details_table,
                   'search_form'                    : form,
                   'user_analysis_details'          : user_analysis_details,
                   'can_edit'                       : can_edit,
                   'is_demo_user'                   : is_demo_user,
                   'is_monitor'                     : is_monitor,
                   'search'                         : search,
                   'auth_pages'                     : authorized_page_list
                  })
