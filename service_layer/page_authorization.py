# -*- coding: utf-8 -*-

import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from ip_analysis.models import Subscriber
from persistance.page_authorization import SubscriberPageAuth
from persistance.user_access_list import UserAccessStatus, UserAccessType, \
    UserAccessList


def add_user_access_status(user_id, access_status, access_type, subscriber):
    listing_status      = UserAccessStatus.objects.get(id = 2)
    listing_type        = UserAccessType.objects.get(id = 1)
    if access_status == 'Blacklist':
        listing_type        = UserAccessType.objects.get(id = 2)
    if access_type == 'Temporary':
        listing_status      = UserAccessStatus.objects.get(id = 1)

    try:
        instance = UserAccessList.objects.get(sid = subscriber, user_id = user_id)
        if instance:
            instance.sid    = subscriber
            instance.user_id= user_id
            instance.type   = listing_type
            instance.status = listing_status
            instance.save()
        return {'instance': instance,}
    except Exception as e:
        created = UserAccessList.objects.create(sid = subscriber,
                                                user_id = user_id,
                                                type = listing_type,
                                                status = listing_status,
                                                change_dt = datetime.datetime.utcnow())

        return {'created': created,}

def delete_user_access_status(instance_id):
    try:
        UserAccessList.objects.get(pk = instance_id).delete()
        return True
    except ObjectDoesNotExist:
        return False

def get_user_access_status_list(subscriber, user_id):

    user_access_status_query = UserAccessList.objects.filter(status = UserAccessStatus.objects.get(id=2))
    query = Q(sid=subscriber)

    if user_id:
        query = query & Q(user_id = user_id, status = UserAccessStatus.objects.get(id=2))
        return user_access_status_query.filter(query)

    return user_access_status_query.filter(query)

def get_authorized_pages(subscriber):
    sid = Subscriber.objects.get(internal_sid = subscriber.pk)
    pages = SubscriberPageAuth.objects.filter(sid = sid)
    list_of_pages = []
    for values in pages:
        list_of_pages.append(values.auth_id.auth_action)
    return list_of_pages
