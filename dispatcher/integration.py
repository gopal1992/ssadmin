from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from dal.integration import get_external_sid
from form_layer.integration import DownloadConnectorsForm
from service_layer.intgeration import verifying_integration
from service_layer.page_authorization import get_authorized_pages
from utils.account import is_normal_user, get_subscriber_decorator, is_admin, \
    is_monitor_mode, is_demo_user_account


@require_http_methods(["GET"])
@login_required
@user_passes_test(is_normal_user)
@get_subscriber_decorator
def getting_started_page(request, subscriber):
    can_edit             = any(is_admin(request.user))
    is_monitor           = is_monitor_mode(subscriber,request.user)
    is_demo_user         = is_demo_user_account(request.user)
    authorized_page_list = get_authorized_pages(subscriber)
    return render(request, 'getting_started.html', {
                                                    'can_edit'      : can_edit,
                                                    'is_monitor'    : is_monitor,
                                                    'is_demo_user'  : is_demo_user,
                                                    'auth_pages'    : authorized_page_list
                                                    })

@require_http_methods(["GET"])
@login_required
@user_passes_test(is_normal_user)
@get_subscriber_decorator
def subscriber_details_page(request, subscriber):
    external_sids    = get_external_sid(subscriber)
    can_edit             = any(is_admin(request.user))
    is_monitor           = is_monitor_mode(subscriber,request.user)
    is_demo_user         = is_demo_user_account(request.user)
    authorized_page_list = get_authorized_pages(subscriber)
    return render(request, 'subscriber_details.html', {'external_sid'    : external_sids[0],
                                                       'sb_external_sid' : external_sids[1],
                                                       'can_edit'        : can_edit,
                                                       'is_monitor'      : is_monitor,
                                                       'is_demo_user'    : is_demo_user,
                                                       'auth_pages'      : authorized_page_list,
                                                        })

@require_http_methods(["GET"])
@login_required
@user_passes_test(is_normal_user)
@get_subscriber_decorator
def download_connectors_page(request, subscriber): #Download process to be noted
    can_edit             = any(is_admin(request.user))
    is_monitor           = is_monitor_mode(subscriber,request.user)
    is_demo_user         = is_demo_user_account(request.user)
    authorized_page_list = get_authorized_pages(subscriber)
    form = DownloadConnectorsForm(request.POST)
    if form.is_valid():
        pass
    else:
        return render(request, 'download_connectors.html', {'form'          : form,
                                                            'can_edit'      : can_edit,
                                                            'is_monitor'    : is_monitor,
                                                            'is_demo_user'  : is_demo_user,
                                                            'auth_pages'    : authorized_page_list,
                                                            })

@require_http_methods(["GET"])
@login_required
@user_passes_test(is_normal_user)
@get_subscriber_decorator
def verify_integration_page(request, subscriber):
    result, message      = verifying_integration(subscriber)
    can_edit             = any(is_admin(request.user))
    is_monitor           = is_monitor_mode(subscriber,request.user)
    is_demo_user         = is_demo_user_account(request.user)
    authorized_page_list = get_authorized_pages(subscriber)
    return render(request, 'verify_integration.html', {'result'         : result,
                                                       'message'        : message,
                                                       'can_edit'       : can_edit,
                                                       'is_monitor'     : is_monitor,
                                                       'is_demo_user'   : is_demo_user,
                                                       'auth_pages'     : authorized_page_list,
                                                       })
