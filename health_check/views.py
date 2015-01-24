import uuid

from django.core.cache import get_cache
from django.http.response import HttpResponse

from health_check.models import HealthCheck
from utils.constants import RK_HEALTH_CHECK_BASE, \
    RK_HEALTH_CHECK_KEY


def health_check(request):
    """
        1. WRITE a UUID
        2. READ it
        3. DELETE it
    """
    if not request.method == "GET":
        return HttpResponse(status=405)

    # Common Key
    uuid_str = uuid.uuid4()
    # Database Check

    try:
        # Create
        HealthCheck.objects.create(test_key=uuid_str)
        # Read
        health_check = HealthCheck.objects.get(test_key=uuid_str)
        # Remove
        health_check.delete()
    except Exception as e:
        return HttpResponse(content=str(e), status=503)

    # Redis Check
    try:
        redis = get_cache('default').raw_client
        # Create
        redis.hset(RK_HEALTH_CHECK_BASE, RK_HEALTH_CHECK_KEY, uuid_str)
        # Read & Verify
        if not redis.hget(RK_HEALTH_CHECK_BASE, RK_HEALTH_CHECK_KEY) == str(uuid_str):
            raise Exception("Redis Read failed.")
        # Remove
        redis.hdel(RK_HEALTH_CHECK_BASE, RK_HEALTH_CHECK_KEY)
    except Exception as e:
        return HttpResponse(content=str(e), status=503)

    # All are success
    return HttpResponse()