# coding: utf-8

# TODO: reverse get

from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict

from stored_filters import create_filter, filters_as_Q

from .models import ACL
from .acl import match_acl
from stored_filters.query import QueryBuilder


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

def has_perm(user, action, instance):
    options = instance._meta
    model = ContentType.objects.get_by_natural_key(
        app_label=options.app_label, model=options.module_name).model_class()
    queryset = model.objects.all()
    available = filter_available(to=user, action=action, queryset=queryset)
    return available.filter(pk=instance.pk).exists()

def get_filter_query(user, action, app_label, model_name):
    """Get query as Q object for filtering objects.
    to -- user instance
    action -- action name
    app_label -- model's app_label
    model_name -- model's name

    @return Q-object or None
    """
    user_acls = match_acl(user, action, app_label, model_name)
    lookups = [acl.lookup for acl in user_acls]
    user_as_dict = model_to_dict(user)
    return filters_as_Q(filters=lookups, context=user_as_dict)

def create_permission(user=None, group=None, action='',
                      conditions=None, exclusions=None,
                      model_class=None, app_label=None, model_name=None):

    lookup = create_filter(conditions, exclusions,
        model_class, app_label, model_name)

    ACL.objects.create(user=user, group=group, action=action, lookup=lookup)

def get_permissions_owner(model_class=None, app_label=None, model_name=None,
                          action=None):
    pass

