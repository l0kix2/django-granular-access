# coding: utf-8
from __future__ import unicode_literals
import re
import operator

from django.db.models import Q

class QueryBuilder(object):

    def __init__(self, user):
        self.user = user

    def convert_lookups_to_Q(self, lookups):
        lookups = self.exclude_blank(lookups)
        if not lookups:
            return None

        return reduce(
            operator.or_,
            map(self.merge_conditions_and_exclusions_to_Q, lookups),
            Q()
        )

    def exclude_blank(self, lookups):
        def is_not_empty(pair):
            return pair['conditions'] is not None or pair['exclusions'] is not None

        return filter(is_not_empty, lookups)

    def merge_conditions_and_exclusions_to_Q(self, lookup_pair):
#        if not lookup_pair['conditions'] and not lookup_pair['exclusions']:
#            return None
        return (
            self.convert_lookup_dicts_list_to_Q(lookup_pair['conditions']) &
            ~self.convert_lookup_dicts_list_to_Q(lookup_pair['exclusions'])
        )

    def convert_lookup_dicts_list_to_Q(self, lookup_dicts):
        if not isinstance(lookup_dicts, (list, tuple)):
            lookup_dicts = [lookup_dicts]
        return reduce(
            operator.or_,
            map(self.convert_lookup_dict_to_Q, lookup_dicts),
            Q()
        )

    def convert_lookup_dict_to_Q(self, lookup_dict):
        if lookup_dict is None:
            return Q()
        self.process_macros(lookup_dict)
        return Q(**lookup_dict)

    def process_macros(self, lookup_dict):
        macro_regex = re.compile(r'^%(?P<attribute>\w+)%$')
        for key, value in lookup_dict.iteritems():
            match = macro_regex.match(value)
            if match:
                attribute = match.group('attribute')
                user_attribute_value = getattr(self.user, attribute)
                lookup_dict[key] = user_attribute_value

