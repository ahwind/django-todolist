# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test


def auth_module(module):

    def decorator(user):

        if module in user.get_codename():
            return True
        else:
            raise PermissionDenied

    return user_passes_test(decorator)


def operate():

    def decorator(user):
        if user.is_staff or user.is_superuser:
            return True
        else:
            raise PermissionDenied
    return user_passes_test(decorator)


def auth_owner(user, hid):
    try:
        gethost = SystemInfo.objects.get(pk=hid)
    except:
        raise PermissionDenied

    if user.is_staff or user.is_superuser or gethost.duty_by == user:
        return True
    else:
        raise PermissionDenied

