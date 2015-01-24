# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from customer_support.views import update_existing_subscriber, \
    add_new_subscriber

from .views import (EditSubscriberView,
                    DeActivateSubscriberView,
                    ReActivateSubscriberView,
                    SupportSubscriberReportView,
                    DashboardView)


urlpatterns = patterns('',
    url(
        regex=r'new_subscriber/$',
        view=add_new_subscriber,
        name="support.new_subscriber"
    ),
    url(
        regex=r'update_subscriber/(?P<pk>\d+)/$',
        view=update_existing_subscriber,
        name="support.update_subscriber"
    ),
    url(
        regex=r'edit_subscriber/$',
        view=EditSubscriberView.as_view(),
        name="support.edit_subscriber"
    ),
    url(
        regex=r'deactivate_subscriber/$',
        view=DeActivateSubscriberView.as_view(),
        name="support.deactivate_subscriber"
    ),
    url(
        regex=r'reactivate_subscriber/$',
        view=ReActivateSubscriberView.as_view(),
        name="support.reactivate_subscriber"
    ),
    url(
        regex=r'reports/$',
        view=SupportSubscriberReportView.as_view(),
        name="support.subscriber_report"
    ),
    url(
        regex=r'dashboard/$',
        view=DashboardView.as_view(),
        name="support.dashboard"
    ),
)
