# coding: utf-8
from __future__ import unicode_literals
from django.db.models.query import QuerySet

from .access import filter_available
from .settings import CONSIDER_SUPERUSER

class AccessQuerySet(QuerySet):
    def available(self, to, action):
        if check_superuser(user=to):
            return self
        return filter_available(to=to, action=action, queryset=self)

class AccessQuerySetMixin(object):
    def available(self, to, action):
        if check_superuser(user=to):
            return self
        return filter_available(to=to, action=action, queryset=self)

def check_superuser(user):
    if CONSIDER_SUPERUSER:
        return user.is_superuser
    return False
