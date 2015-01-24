from django.db.models.aggregates import Sum
from django.db.models.query_utils import Q

from aggregator_analysis.models import AggregatorAnalysis
from ip_analysis.service.ip_analysis_details import convert_date_specific_to_timezone
from ip_analysis.views import _get_date_from_timestamp


def get_base_results_for_aggregator_analysis_excel(request, subscriber):
    """
    This function accepts the "Start Date" and "End Date" and returns the corresponding Aggreggator analysis values
    which is then send to excel_view_aggregator_ip_analysis for excel sheet value population.
    """
    start_date_utc       = request.GET.get('date_from')
    end_date_utc         = request.GET.get('date_to')
    start_date, end_date = _get_date_from_timestamp(request, start_date_utc, end_date_utc)

    search_ip_address       = None
    search_aggregator_name  = None

    start_date, end_date = convert_date_specific_to_timezone(subscriber.timezone, start_date, end_date)
    aggregator_ip_analysis_data = get_aggregator_analysis_details(subscriber,
                                                                  search_ip_address,
                                                                  search_aggregator_name,
                                                                  start_date,
                                                                  end_date)
    result = {'aggregator_ip_analysis': aggregator_ip_analysis_data, }
    return result

def get_aggregator_analysis_details(subscriber,
                                    ip_address,
                                    aggregator_name,
                                    date_from,
                                    date_to):
    """
    This function is a shared function which attends to the search bar operations and also excel download sheet data retrieval
    """
    aggregator_analysis_query = AggregatorAnalysis.objects.all() \
                                          .values('ip_address')\
                                          .annotate(total_requests = Sum('total_requests'))\
                                          .order_by("-total_requests")

    query = Q(sid=subscriber) & Q(dt__range=[date_from, date_to])

    if ip_address:
        query = query & Q(ip_address__ip_address__icontains=ip_address)
        return aggregator_analysis_query.filter(query)

    if aggregator_name:
        query = query & Q(ip_address__aggregator_name__icontains=aggregator_name)
        return aggregator_analysis_query.filter(query)

    # Return all the records for the subscriber
    return aggregator_analysis_query.filter(query)