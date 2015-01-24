# -*- coding: utf-8 -*-

from functools import wraps

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from ip_analysis.models import UserSubscriber, Subscriber


class GROUPS:
    SHIELD_SQUARE_SUPER_ADMIN       = "shield_square_super_admin"
    SHIELD_SQUARE_CUSTOMER_SUPPORT  = "shield_square_customer_support"
    SUBSCRIBER_ADMIN                = "subscriber_admin"
    SUBSCRIBER_USER                 = "subscriber_user"
    DEMO_USER                       = "demo_user"

ADMIN_GROUPS        = [GROUPS.SHIELD_SQUARE_SUPER_ADMIN,
                       GROUPS.SUBSCRIBER_ADMIN]
SHIELD_SQUARE_USER  = [GROUPS.SHIELD_SQUARE_SUPER_ADMIN,
                       GROUPS.SHIELD_SQUARE_CUSTOMER_SUPPORT]
DEMO_USER           = [GROUPS.DEMO_USER,]

def is_shield_square_user(user):
    return user.groups.filter(name__in=SHIELD_SQUARE_USER) or user.is_superuser


class ShieldSquareUserMixin(object):
    def dispatch(self, *args, **kwargs):
        if is_shield_square_user(self.request.user):
            return super(ShieldSquareUserMixin, self).dispatch(*args, **kwargs)
        logout(self.request)
        return redirect(reverse('accounts.login'))


def get_subscriber_from_user(request):
    user = request.user
    try:
        return UserSubscriber.objects.get(user=user).subscriber
    except ObjectDoesNotExist:
        # Super User
        if request.session.get('is_support'):
            sid = request.session.get('sid')
            if sid:
                return Subscriber.objects.get(internal_sid=sid)
        return None


def get_subscriber_decorator(f):
    @wraps(f)
    def wrapped_f(request, *args, **kwargs):
        subscriber = get_subscriber_from_user(request)
        return f(request, subscriber, *args, **kwargs)
    return wrapped_f

def is_admin(user):
    return user.groups.filter(name__in=ADMIN_GROUPS)

def is_demo_user_account(user):
    """ Returns True if the given user has demo_user configured """
    if user.groups.filter(name__in=DEMO_USER):
        return True
    return False

def is_normal_user(user):
    groups = ADMIN_GROUPS[:]
    groups.extend(SHIELD_SQUARE_USER)
    groups.extend(["subscriber_user"])
    return user.groups.filter(name__in=groups) or user.is_staff


def is_monitor_mode(subscriber,user):
    # For Demo1 user Monitor mode
    if str(user) == 'demo1@shieldsquare.com':
        return True
    # For Demo2 user Active mode
    elif not str(user) == 'demo2@shieldsquare.com':
        if subscriber.mode == 1:
            return True
        return False
    return False


def is_shield_square_admin(user):
    return user.group.filter(name=GROUPS.SHIELD_SQUARE_SUPER_ADMIN)
