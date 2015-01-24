#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group


GROUP_NAMES = ["subscriber_admin",
               "subscriber_user",
               "shield_square_customer_support",
               "shield_square_super_admin",
               "demo_user"]

def create_groups():
    for group in GROUP_NAMES:
        Group.objects.get_or_create(name=group)


if __name__ == "__main__":
    create_groups()
