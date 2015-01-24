# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from ip_analysis.models import IpAddressAccessList, IpAccessType


def add_ip_access_status(ip_address, access_status, subscriber):
    listing_type = IpAccessType.objects.get(id=1)
    instance, created = IpAddressAccessList.objects.get_or_create(sid=subscriber,
                                                                  ipaddress=ip_address,
                                                                  type = listing_type)
    if instance:
        instance.sid = subscriber
        instance.ipaddress = ip_address
        instance.type = listing_type
        instance.save

    return {'instance': instance, 'created': created}

def delete_ip_access_status(instance_id):
    """ Need to check against the user's subscriber to prevent other subscriber's
        instance id deletion.
    """
    try:
        IpAddressAccessList.objects.get(pk = instance_id).delete()
        return True
    except ObjectDoesNotExist:
        return False

def get_ip_access_status_list(subscriber,
                              ip_address):

    # Filter from the IpAddressAccessList table for SID, ip_address & access_status
    ip_access_status_query = IpAddressAccessList.objects.all()
    query = Q(sid=subscriber)

    if ip_address:
        query = query & Q(ipaddress__icontains=ip_address)
        return ip_access_status_query.filter(query)

    return ip_access_status_query.filter(query) # Return all the records for the subscriber
