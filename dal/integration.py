from django.core.exceptions import ObjectDoesNotExist

from ip_analysis.models import Subscriber
from utils.constants import RK_VERIFY

import redis

pool    = redis.ConnectionPool(host='stagprocessdatasa.redis.cache.windows.net', port=6379, db=0, password='R2Qsu5SuHD3qDp+hUVHNU5oSRMldd0WLiX7fw2Xmgas=')
r       = redis.StrictRedis(connection_pool=pool)

def get_external_sid(subscriber):
    try:
        subscriber = Subscriber.objects.get(internal_sid = subscriber.internal_sid)
        return subscriber.external_sid, subscriber.sb_external_sid
    except ObjectDoesNotExist:
        return False

def get_integration_details(subscriber):
    base_key = "{}:{}".format(RK_VERIFY, subscriber.sb_internal_sid)
    packets  = r.lrange(base_key, 0, 4)
    return packets

def get_smembers(key):
    return r.smembers(key)
