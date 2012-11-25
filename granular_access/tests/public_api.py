# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from .base import BaseTest

from stored_filters import create_filter
from granular_access.models import ACL
from granular_access.access import get_filter_query, filter_available
from granular_access.access import create_permission, has_perm

class PublicApiTest(BaseTest):
    def setUp(self):
        self.batman = User.objects.create_user(username='batman',
                                               email='batman@gotham.us')
        self.joker = User.objects.create_user(username='joker',
                                              email='joker@gotham.us')
        self.god = User.objects.create_user(username='god',
                                            email='god@gmail.com')

        lookup = create_filter(model_class=User,
            conditions=[{'username__startswith': 'joker'}])
        ACL.objects.create(user=self.batman, group=None,
                           lookup=lookup, action='edit')

        blank_lookup = create_filter(model_class=User,
            conditions=None, exclusions=None)
        ACL.objects.create(user=self.joker, group=None,
                           lookup=blank_lookup, action='edit')

        god_lookup = create_filter(model_class=User,
            conditions={}, exclusions=None)
        ACL.objects.create(user=self.god, group=None,
                           lookup=god_lookup, action='edit')

    def test_get_filter_query(self):
        query = get_filter_query(user=self.batman, action='edit',
                                 app_label='auth', model_name='user')

        self.assertQuerysetEqualsList(
            User.objects.filter(query),
            [self.joker]
        )

    def test_get_filter_query_blank_lookups(self):


        query = get_filter_query(user=self.joker, action='edit',
                                 app_label='auth', model_name='user')

        self.assertIsNone(query)

    def test_filter_available(self):
        filtered = filter_available(to=self.batman, action='edit',
                                    queryset=User.objects.all())

        self.assertQuerysetEqualsList(
            filtered,
            [self.joker]
        )

    def test_has_perm(self):
        self.assertTrue(
            has_perm(user=self.batman, action='edit', instance=self.joker)
        )

    def test_has_no_perm(self):
        self.assertFalse(
            has_perm(user=self.batman, action='edit', instance=self.god)
        )

    def test_filter_available_blank_query(self):
        filtered = filter_available(to=self.joker, action='edit',
                                    queryset=User.objects.all())

        self.assertQuerysetEqualsList(filtered, [])

    def test_filter_available_super_query(self):
        filtered = filter_available(to=self.god, action='edit',
                                    queryset=User.objects.all())

        self.assertQuerysetEqualsList(
            filtered,
            [self.god, self.batman, self.joker]
        )

    def test_create_permission_using_model(self):
        conditions = [{'some_condition': 'value'}]
        action = 'some_action'

        create_permission(user=self.batman, action=action,
            conditions=conditions, model_class=User)

        user_content_type = ContentType.objects.get_for_model(User)
        self.assertTrue(
            ACL.objects.filter(action=action, user=self.batman,
                lookup__content_type=user_content_type).exists()
        )

    def test_create_permission_using_ct_natural_key(self):
        conditions = [{'some_condition': 'value'}]
        action = 'some_action'

        create_permission(user=self.batman, action=action,
            conditions=conditions, app_label='auth', model_name='user')

        user_content_type = ContentType.objects.get_for_model(User)
        self.assertTrue(
            ACL.objects.filter(action=action, user=self.batman,
                lookup__content_type=user_content_type).exists()
        )
