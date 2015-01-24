# -*- coding: utf-8 -*-

import string
import random

from pytz import common_timezones

from django.contrib.auth.models import User, Group
from django.db import IntegrityError


ALLOWED_CHARS = string.ascii_uppercase + string.ascii_lowercase


def update_timezone_for_subscriber(subscriber, timezone):
    if timezone in common_timezones:
        subscriber.timezone = timezone
        subscriber.save()
        return True
    return False

def generate_random_password(size=10, allowed_chars=ALLOWED_CHARS):
    return ''.join(random.choice(allowed_chars) for _ in range(size))

def create_user_without_password(email, username=None):
    try:
        return User.objects.create(email=email,
                                   username=username or email,
                                   password=generate_random_password())
    except IntegrityError:
        return False

def delete_user_by_email(email):
    try:
        User.objects.get(username=email).delete()
        return True
    except User.DoesNotExist:
        return False
    except User.MultipleObjectsReturned:
        return False

def get_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return False
    except User.MultipleObjectsReturned:
        return False

def grant_privilege(user, privilege):
    admin_group = Group.objects.get(name="subscriber_admin")
    user_group = Group.objects.get(name="subscriber_user")
    if privilege == "user":
        user_group.user_set.add(user)
    elif privilege == "admin":
        admin_group.user_set.add(user)
    user.save()

def modify_privilege(user, privilege):
    admin_group = Group.objects.get(name="subscriber_admin")
    user_group = Group.objects.get(name="subscriber_user")
    if privilege == "user":
        if not user.groups.filter(name="subscriber_user").count():
            admin_group.user_set.remove(user)
            user_group.user_set.add(user)
    elif privilege == "admin":
        if not user.groups.filter(name="subscriber_admin").count():
            user_group.user_set.remove(user)
            admin_group.user_set.add(user)
    user.save()
