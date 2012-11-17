# coding: utf-8
from __future__ import unicode_literals

from django.db.models import Manager

from .queryset import AccessQuerySet, check_superuser
from .access import filter_available

class AccessManager(Manager):
    def get_query_set(self):
        return AccessQuerySet(model=self.model, using=self._db)

    def available(self, *args, **kwargs):
        return self.get_query_set().available(*args, **kwargs)

class AccessManagerMixin(object):
    def available(self, to, action):
        queryset = self.get_query_set()
        if check_superuser():
            return queryset
        return filter_available(to=to, action=action, queryset=queryset)
