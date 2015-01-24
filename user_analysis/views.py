import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from service_layer import page_authorization
from service_layer.page_authorization import get_authorized_pages
from user_analysis.forms import UserAccessStatusForm, UserAccessStatusDeleteForm, \
    UserAccessStatusSearchForm
from user_analysis.models import UserAccessList
from utils.account import get_subscriber_decorator, is_admin, \
    is_demo_user_account, is_monitor_mode
from utils.decorator import access_to_page


@require_http_methods(["POST"])
@login_required
@get_subscriber_decorator
def add_user_access_status(request, subscriber):
    form = UserAccessStatusForm(request.POST)
    access_status   = 'Whitelist' if int(form.data['access_status']) == 1 else 'Blacklist'
    access_type     = 'Permanent' if int(form.data['access_type']) == 1 else 'Temporary'
    if form.is_valid():
        # Call service layer to persist
        page_authorization.add_user_access_status(form.data['user_id_add'],
                                                  access_status,
                                                  access_type,
                                                  subscriber)

        access_type     = 'permanently' if access_type == 'Permanent' else 'temporarily'
        access_status   = 'Whitelisted' if access_status == 'Whitelist' else 'Blacklisted'

        messages.success(request, "Successfully {} the User ID '{}' {}.".format(access_status,
                                                                        form.data['user_id_add'],
                                                                        access_type))

#         user = request.user
#         if user.email:
#             send_templated_email(
#                 label   = "user_access",
#                 to      = user.email,
#                 context = {"action" : access_status,
#                            "type"   : access_type,
#                            "user_id": form.data['user_id_add']})
#         else:
#             # Fail silently for now
#             pass

        data = {'result': True,}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    # end if
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["POST"])
@login_required
@get_subscriber_decorator
def delete_user_access_status(request, subscriber, instance_id):
    form = UserAccessStatusDeleteForm(request.POST)
    if form.is_valid():
        user_access = UserAccessList.objects.get(pk = instance_id)
        # Call service layer to delete
        deleted = page_authorization.delete_user_access_status(instance_id)
        data = {'result': True,}
        if deleted:
            messages.success(request, "Successfully deleted the User ID '{}' from {} Whitelisting"\
                            .format(user_access.user_id, user_access.status.status))

#             # Send E-Mail Notification
#             user = request.user
#             if user.email:
#                 send_templated_email(
#                     label="user_access",
#                     to=user.email,
#                     context={"action"   : "deleted",
#                              "user_id"  : user_access.user_id,
#                              "type"     : user_access.type.type})
#             else:
#                 # Fail silently for now
#                 pass
        else: # Record is already available and updated
            data = {'result': False,
                    'errors': "Failed to delete the IP Address."}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    # end if
    data = {'result': False,
            'errors': form.errors}
    return HttpResponse(json.dumps(data), mimetype='application/json')

@require_http_methods(["GET"])
@login_required
@get_subscriber_decorator
@access_to_page('User Access')
def list_user_access_status(request, subscriber):  # @UndefinedVariable
    page_no =   request.GET.get('page', 1)
    form    =   UserAccessStatusSearchForm(request.GET)

    search_user_id   = None

    if form.is_valid():
        search_user_id   = form.cleaned_data['user_id']


    # Call service layer to persist
    paginator = Paginator(page_authorization.get_user_access_status_list(subscriber, search_user_id),15)
    user_access_status_list = None

    try:
        user_access_status_list = paginator.page(page_no)
    except PageNotAnInteger:
        user_access_status_list = paginator.page(page_no)
    except EmptyPage:
        user_access_status_list = paginator.page(paginator.num_pages)

    user_access_status_table = [] # List of dicts for HTML rendering
    for user_access_status in user_access_status_list:
        try:
            user_access_status_table.append({'id'        :   user_access_status.pk,
                                             'user_id'   :   user_access_status.user_id,
                                             'date_added':   user_access_status.change_dt.strftime('%b %d, %Y')
                                             })
        except ObjectDoesNotExist:
            print user_access_status.pk
    # Is search requested -> to display the search boxes if no results found in the search
    search = False
    if any([search_user_id]):
        search = True

    can_edit        = any(is_admin(request.user))
    is_demo_user    = is_demo_user_account(request.user)
    is_monitor      = is_monitor_mode(subscriber,request.user)
    authorized_page_list = get_authorized_pages(subscriber)

    return render(request,
                'user_accesslist.html',
                {
                'user_access_status_table'       : user_access_status_table,
                'user_access_status_search_from' : form,
                'user_access_status_add_form'    : UserAccessStatusForm(),
                'user_access_status_delete_form' : UserAccessStatusDeleteForm(),
                'user_access_status_list'        : user_access_status_list,
                'is_demo_user'                   : is_demo_user,
                'can_edit'                       : can_edit,
                'search'                         : search,
                'is_monitor'                     : is_monitor,
                'auth_pages'                     : authorized_page_list
                }
                )
