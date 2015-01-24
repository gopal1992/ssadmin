#! /usr/bin/env python
# -*- coding: utf-8 -*-
from ip_analysis.models import Subscriber, IpAddressAccessList
from django.http.response import HttpResponse


def update_redis_subscriber():
    for subscriber in Subscriber.objects.all():
        print "Updating Subscriber Data : {}".format(subscriber)
        subscriber.save()

def update_redis_ip_access_list():
    for ip_access in IpAddressAccessList.objects.all():
        print "Updating IP Access List :{}".format(ip_access)
        ip_access.save()


if __name__ == "__main__":
    print "Begin : Updating the Redis from RDBMS"
    update_redis_subscriber()
    update_redis_ip_access_list()
    print "End : Updating the Redis from RDBMS"

def update_redis(request):
    if not request.user.is_superuser:
        return HttpResponse("Not Authorized.")

    update_redis_subscriber()
    update_redis_ip_access_list()
    return HttpResponse("End : Updated the Redis from RDBMS")
