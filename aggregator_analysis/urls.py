from django.conf.urls import patterns, url
from django.contrib import admin

from aggregator_analysis.views import list_aggregator_analysis_details, \
    excel_view_aggregator_analysis


admin.autodiscover()

urlpatterns = patterns('',
    url(
        regex=r'aggregator_analysis/$',
        view=list_aggregator_analysis_details,
        name="list_aggregator_analysis_details"
    ),
    url(
        regex=r'aggregator_analysis/excel/$',
        view=excel_view_aggregator_analysis,
        name="aggregator_analysis.excel_view_aggregator_analysis"
    ),
)