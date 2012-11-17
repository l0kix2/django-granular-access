# coding: utf-8

# TODO: jsonfield lib
# TODO: reverse get

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from .models import ModelLookup, ACL
from .acl import match_acl, fetch_lookups
from .query import QueryBuilder


def filter_available(to, action, queryset):
    """Filter objects, available to user for specified action.
    to -- user instance
    action -- action name
    queryset -- base queryset for filtering

    """
    app_label = queryset.model._meta.app_label
    model_name = queryset.model._meta.module_name
    query = get_filter_query(user=to, action=action,
                             app_label=app_label, model_name=model_name)
    if query is None:
        return queryset.none()
    return queryset.filter(query)

def get_filter_query(user, action, app_label, model_name):
    """Get query as Q object for filtering objects.
    to -- user instance
    action -- action name
    app_label -- model's app_label
    model_name -- model's name

    @return Q-object or None
    """
    user_acls = match_acl(user, action, app_label, model_name)
    lookups = fetch_lookups(user_acls)
    return QueryBuilder(user).convert_lookups_to_Q(lookups)

def create_permission(user=None, group=None, action='',
                      conditions=None, exclusions=None,
                      model_class=None, app_label=None, model_name=None):
    if model_class:
        content_type = ContentType.objects.get_for_model(model_class)
    elif app_label and model_name:
        content_type = ContentType.objects.get_by_natural_key(
            app_label=app_label, model=model_name)
    else:
        raise Exception(
            'You should specify model_class or app_label and model_name')

    lookup = ModelLookup.objects.create(
        conditions=conditions, exclusions=exclusions, content_type=content_type
    )

    ACL.objects.create(user=user, group=group, action=action, lookup=lookup)

def get_permissions_owner(model_class=None, app_label=None, model_name=None,
                          action=None):
    pass
