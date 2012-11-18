# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings

USER_MODEL = getattr(settings, 'GRANULAR_ACCESS_USER_MODEL', 'auth.User')
GROUP_MODEL = getattr(settings, 'GRANULAR_ACCESS_GROUP_MODEL', 'auth.Group')

USER_GROUP_RELATED_NAME = getattr(settings,
    'GRANULAR_ACCESS_USER_GROUP_RELATED_NAME', 'groups')

GET_USER_GROUPS_FUNCTION = getattr(settings,
    'GRANULAR_ACCESS_GET_USER_GROUPS_FUNCTION', None)

CONSIDER_SUPERUSER = getattr(settings,
    'GRANULAR_ACCESS_CONSIDER_SUPERUSER', True)

