# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

from data_migration.views import new_view_traffic_analysis, \
    excel_view_traffic_analysis
from dispatcher.integration import getting_started_page, subscriber_details_page, \
    download_connectors_page, verify_integration_page
from dispatcher.registration import registration_process, verifying_registration, \
    resend_verification_link
from dispatcher.user_analysis import list_user_analysis_details, \
    excel_view_user_analysis
from health_check.views import health_check
from ip_analysis.views import list_ip_analysis_details, list_ip_access_status, \
    add_ip_access_status, delete_ip_access_status, \
    add_ip_access_status_for_ip_analysis, \
    update_action_for_ip_analysis, get_ip_details_in_specific_range
from redis_update import update_redis
from user_analysis.views import list_user_access_status, \
    delete_user_access_status, add_user_access_status
from utils.error_handler import server_error_500, exception_raiser_view


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^configuration/', include('ip_analysis.urls')),
    url(r'^support/', include('customer_support.urls', app_name='customer_support')),
    url(r'^aggregator/', include('aggregator_analysis.urls', app_name='aggregator_analysis')),

    # Registration Process
    url(r'^registration/', registration_process, name='registration_process'),
    url(r'^resend_verification/', resend_verification_link, name='resend_verification_link'),
    url(r'^verifying_registration/(?P<activation_link>[\w$-]+)/$', verifying_registration, name='verifying_registration'),

    # Integration Process
    url(r'^getting_started/', getting_started_page, name='getting_started_page'),
    url(r'^subscriber_details/', subscriber_details_page, name='subscriber_details_page'),
    url(r'^download_connectors/', download_connectors_page, name='subscriber_details_page'),
    url(r'^verify_integration/', verify_integration_page, name='subscriber_details_page'),

    url(r'^ip_analysis/', list_ip_analysis_details, name='ip_analysis.ip_analysis'),
    url(r'^ip_analysis_action_change/', view = update_action_for_ip_analysis),
    url(r'^ip_analysis_list_ip_details/',view = get_ip_details_in_specific_range),

    url(r'^ip_access_list/', list_ip_access_status, name="ip_access_list"),
    url(r'^ip_access_status_add/', add_ip_access_status),
    url(r'^ip_access_status_change/', add_ip_access_status_for_ip_analysis),
    url(r'^ip_access_status_delete/(?P<instance_id>\d+)/$', delete_ip_access_status),

    # User Analysis page urls
    url(r'^user_analysis/$', list_user_analysis_details, name='user_analysis.view_user_analysis'),
    url(r'^user_analysis/excel/$', excel_view_user_analysis, name='user_analysis.excel_view_user_analysis'),

    # User Access List page urls
    url(r'^user_access_list/', list_user_access_status, name="user_access_list"),
    url(r'^user_access_status_add/', add_user_access_status),
    url(r'^user_access_status_delete/(?P<instance_id>\d+)/$', delete_user_access_status),

    url(regex=r'traffic_analysis/excel/$', view=excel_view_traffic_analysis, name="data_migration.excel_view_traffic_analysis"),
    url(r'^home/analysis/$', view=new_view_traffic_analysis, name="ip_analysis.view_traffic_analysis"),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^update-redis/$', update_redis),
    url(r'^getStatus/$', health_check),

    # Exception Point
    url(r'^ex/', exception_raiser_view, name='exception_raiser_view'),

    # Do not use any url beyond this url
    url(r'', view=new_view_traffic_analysis, name="ip_analysis.view_traffic_analysis"),

)

handler500 = server_error_500
