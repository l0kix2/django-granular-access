# coding: utf-8
from __future__ import unicode_literals
from django.db.models import Q

from .models import ACL
from .settings import  GET_USER_GROUPS_FUNCTION as GET_GROUPS
from .settings import  USER_GROUP_RELATED_NAME as RELATED_NAME
from .utils import get_function_by_path

def match_acl(user, action, app_label, model_name):
    user_groups = get_user_groups(user=user)

    user_query = (
        Q(user=user) |
        Q(group__in=user_groups) |
        Q(user__isnull=True) & Q(group__isnull=True)
    )
    model_query = (
        Q(lookup__content_type__model=model_name) &
        Q(lookup__content_type__app_label=app_label)
    )
    action_query = Q(action=action) | Q(action='')

    return ACL.objects.select_related('lookup').filter(
        user_query, model_query, action_query)

def get_user_groups(user):
    if GET_GROUPS is None:
        groups_related_manager = getattr(user, RELATED_NAME)
        return groups_related_manager.all()
    else:
        group_getter = get_function_by_path(GET_GROUPS)
        return group_getter(user)

