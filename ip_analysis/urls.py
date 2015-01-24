# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import (view_bot_response,
                    add_pages_per_minute,
                    add_pages_per_session,
                    add_session_length,
                    add_browser_integrity_check,
                    add_http_request_integrity_check,
                    add_aggregator_bot_traffic_check,
                    add_behaviour_integrity_check,
                    excel_view_ip_analysis)


urlpatterns = patterns('',
    url(
        regex=r'bot/pages_per_minute/$',
        view=add_pages_per_minute,
        name="ip_analysis.add_pages_per_minute"
    ),
    url(
        regex=r'bot/pages_per_session/$',
        view=add_pages_per_session,
        name="ip_analysis.add_pages_per_session"
    ),
    url(
        regex=r'bot/session_length/$',
        view=add_session_length,
        name="ip_analysis.add_session_length"
    ),
    url(
        regex=r'bot/browser_integrity_check/$',
        view=add_browser_integrity_check,
        name="ip_analysis.add_browser_integrity_check"
    ),
    url(
        regex=r'bot/http_request_integrity_check/$',
        view=add_http_request_integrity_check,
        name="ip_analysis.add_http_request_integrity_check"
    ),
    url(
        regex=r'bot/aggregator_check/$',
        view=add_aggregator_bot_traffic_check,
        name="ip_analysis.add_aggregator_bot_traffic_check"
    ),
    url(
        regex=r'bot/behaviour_integrity_check/$',
        view=add_behaviour_integrity_check,
        name="ip_analysis.add_behaviour_integrity_check"
    ),
    url(
        regex=r'bot/$',
        view=view_bot_response,
        name="ip_analysis.view_bot_response"
    ),
    url(
        regex=r'ip_analysis/excel/$',
        view=excel_view_ip_analysis,
        name="ip_analysis.excel_view_ip_analysis"
    ),
)
