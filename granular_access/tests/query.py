# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User

from .base import BaseTest
from granular_access.query import QueryBuilder


class LookupConvertionTest(BaseTest):
    def setUp(self):
        self.batman = User.objects.create_user(username='batman',
                                               email='batman@gotham.us')
        self.joker = User.objects.create_user(username='joker',
                                              email='joker@gotham.us')
        self.builder = QueryBuilder(user=self.batman)

    def test_process_macros(self):
        lookup_dict = {'username': '%username%',
                       'email': '%email%',
                       'some_field': 'some_value'}

        self.builder.process_macros(lookup_dict)

        self.assertEqual(lookup_dict, {
            'username': 'batman',
            'email': 'batman@gotham.us',
            'some_field': 'some_value'
        })

    def test_convert_lookup_dict_to_Q(self):
        lookup_dict = {'username__startswith': 'bat',
                       'email__endswith': 'us'}

        query = self.builder.convert_lookup_dict_to_Q(lookup_dict)

        self.assertQuerysetEqualsList(
            User.objects.filter(query),
            [self.batman]
        )

    def test_convert_lookup_dicts_list_to_Q(self):
        lookup_dicts = [
            {'username__startswith': 'bat'},
            {'email__endswith': 'gotham.us'},
        ]
        query = self.builder.convert_lookup_dicts_list_to_Q(lookup_dicts)

        self.assertQuerysetEqualsList(
            User.objects.filter(query),
            [self.batman, self.joker]
        )

    def test_convert_lookup_dicts_list_to_Q_not_list(self):
        alone_dict = {'username__startswith': 'bat'}

        query = self.builder.convert_lookup_dicts_list_to_Q(alone_dict)

        self.assertQuerysetEqualsList(
            User.objects.filter(query),
            [self.batman]
        )

    def test_merge_conditions_and_exclusions_to_Q(self):
        lookup_pair = {
            'conditions': [{'email__endswith': 'gotham.us'}],
            'exclusions': [{'username__startswith': 'bat'}],
        }
        query = self.builder.merge_conditions_and_exclusions_to_Q(lookup_pair)

        self.assertQuerysetEqualsList(
            User.objects.filter(query),
            [self.joker]
        )

    def test_merge_conditions_and_exclusions_to_Q_conditions_only(self):
        lookup_pair = {
            'conditions': [{'email__endswith': 'gotham.us'}],
            'exclusions': None,
        }
        query = self.builder.merge_conditions_and_exclusions_to_Q(lookup_pair)

        self.assertQuerysetEqualsList(
            User.objects.filter(query),
            [self.batman, self.joker]
        )

    def test_merge_conditions_and_exclusions_to_Q_exclusions_only(self):
        lookup_pair = {
            'conditions': None,
            'exclusions': [{'username__startswith': 'bat'}],
        }

        query = self.builder.merge_conditions_and_exclusions_to_Q(lookup_pair)

        self.assertQuerysetEqualsList(
            User.objects.filter(query),
            [self.joker]
        )

#    def test_merge_conditions_and_exclusions_to_Q_blank_filters(self):
#        lookup_pair = {
#            'conditions': None,
#            'exclusions': None,
#        }
#
#        query = self.builder.merge_conditions_and_exclusions_to_Q(lookup_pair)
#
#        self.assertIsNone(query)

    def test_convert_lookups_to_Q(self):
        lookups = [{
            'conditions': [{'username__startswith': 'batman'}],
            'exclusions': [{'email__startswith': 'j'}],
        },{
            'conditions': [{'username__startswith': 'joker'}],
            'exclusions': None,
        }]

        query = self.builder.convert_lookups_to_Q(lookups)

        self.assertQuerysetEqualsList(
            User.objects.filter(query),
            [self.batman, self.joker]
        )

    def test_convert_lookups_to_Q_with_blank_filters(self):
        lookups = [{
            'conditions': [{'username__startswith': 'batman'}],
            'exclusions': [{'email__startswith': 'j'}],
        },{
            'conditions': None,
            'exclusions': None,
        }]

        query = self.builder.convert_lookups_to_Q(lookups)

        self.assertQuerysetEqualsList(
            User.objects.filter(query),
            [self.batman]
        )
