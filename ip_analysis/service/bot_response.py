# -*- coding: utf-8 -*-
from ip_analysis.models import ResponseCode


def update_pages_per_session(subscriber, pages_per_session, action):
    rc = ResponseCode.objects.get(id=int(action))
    if not subscriber.pagepersess == pages_per_session:
        subscriber.pagepersess = pages_per_session
        subscriber.save()
        return 1
    if not subscriber.r_pagepersess == rc:
        subscriber.r_pagepersess = rc
        subscriber.save()
        return 1
    return 0


def update_pages_per_minute(subscriber, pages_per_minute, action):
    rc = ResponseCode.objects.get(id=int(action))
    if not subscriber.pagepermin == pages_per_minute:
        subscriber.pagepermin = pages_per_minute
        subscriber.save()
        return 1
    if not subscriber.r_Pagepermin == rc:
        subscriber.r_Pagepermin = rc
        subscriber.save()
        return 1
    return 0


def update_session_length(subscriber, session_length, action):
    rc = ResponseCode.objects.get(id=int(action))
    if not subscriber.sesslength == session_length:
        subscriber.sesslength = session_length
        subscriber.save()
        return 1
    if not subscriber.r_sesslength == rc:
        subscriber.r_sesslength = rc
        subscriber.save()
        return 1
    return 0


def update_bot_category_check(subscriber, action, field):
    rc = ResponseCode.objects.get(id=int(action))
    if field == "behaviour":
        subscriber.r_behaviourIntegrity = rc
    elif field == "http_request":
        subscriber.r_httpRequestIntegrity = rc
    elif field == "aggregator":
        subscriber.r_Aggregator = rc
    elif field == "browser_integrity":
        subscriber.r_browserIntgrity = rc
    elif field == "rate_limiting":
        subscriber.r_Pagepermin = rc

    subscriber.save()
