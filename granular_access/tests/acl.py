# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

from stored_filters.models import Filter
from granular_access.models import ACL
from granular_access.tests.base import BaseTest
from granular_access.acl import match_acl

class MatchACLTest(BaseTest):
    def setUp(self):
        self.batman = User.objects.create_user(username='batman')
        self.joker = User.objects.create_user(username='joker')
        self.superheroes = Group.objects.create(name='superheroes')

        self.lookup = Filter.objects.create(
            content_type=ContentType.objects.get_for_model(User))

    def test_user_personal_acl(self):
        acl1 = ACL.objects.create(user=self.batman, group=None,
                                  lookup=self.lookup, action='')

        matched = match_acl(user=self.batman, action='save',
                            model_name='user', app_label='auth')

        self.assertQuerysetEqualsList(matched, [acl1])

    def test_group_acl(self):
        self.superheroes.user_set.add(self.batman)
        acl1 = ACL.objects.create(user=None, group=self.superheroes,
                                  lookup=self.lookup, action='')

        matched = match_acl(user=self.batman, action='save',
                            model_name='user', app_label='auth')

        self.assertQuerysetEqualsList(matched, [acl1])

    def test_kill_and_rob_acl(self):
        acl1 = ACL.objects.create(user=None, group=None,
                                  lookup=self.lookup, action='')

        matched = match_acl(user=self.batman, action='save',
                            model_name='user', app_label='auth')

        self.assertQuerysetEqualsList(matched, [acl1])

    def test_user_or_group_acl(self):
        """weird looking, but should work"""
        acl1 = ACL.objects.create(user=self.batman, group=self.superheroes,
                                  lookup=self.lookup, action='')

        matched = match_acl(user=self.batman, action='save',
                            model_name='user', app_label='auth')

        self.assertQuerysetEqualsList(matched, [acl1])

        self.superheroes.user_set.add(self.batman)
        matched = match_acl(user=self.batman, action='save',
                            model_name='user', app_label='auth')

        self.assertQuerysetEqualsList(matched, [acl1])

    def test_permissionless_user(self):
        ACL.objects.create(user=self.batman, group=None,
                           lookup=self.lookup, action='')

        matched = match_acl(user=self.joker, action='save',
                            model_name='user', app_label='auth')

        self.assertQuerysetEqualsList(matched, [])

    def test_action_match(self):
        acl1 = ACL.objects.create(user=None, group=None,
                                  lookup=self.lookup, action='kill-rob')

        matched = match_acl(user=self.joker, action='kill-rob',
                            model_name='user', app_label='auth')

        self.assertQuerysetEqualsList(matched, [acl1])

    def test_action_mismatch(self):
        ACL.objects.create(user=None, group=None,
                           lookup=self.lookup, action='kill-rob')

        matched = match_acl(user=self.joker, action='save',
                            model_name='user', app_label='auth')

        self.assertQuerysetEqualsList(matched, [])

    def test_action_wildcard_match(self):
        acl1 = ACL.objects.create(user=None, group=None,
                                  lookup=self.lookup, action='')

        matched = match_acl(user=self.joker, action='kill-rob',
                            model_name='user', app_label='auth')

        self.assertQuerysetEqualsList(matched, [acl1])

    def test_model_match(self):
        acl1 = ACL.objects.create(user=None, group=None,
                                  lookup=self.lookup, action='')

        matched = match_acl(user=self.joker, action='kill-rob',
                            model_name='user', app_label='auth')

        self.assertQuerysetEqualsList(matched, [acl1])

    def test_model_mismatch(self):
        ACL.objects.create(user=None, group=None,
                            lookup=self.lookup, action='')

        matched = match_acl(user=self.joker, action='kill-rob',
                            model_name='group', app_label='auth')

        self.assertQuerysetEqualsList(matched, [])

    def test_full_case(self):
        self.superheroes.user_set.add(self.batman)

        acl1 = ACL.objects.create(user=self.batman, group=None,
                                  lookup=self.lookup, action='save')
        acl2 = ACL.objects.create(user=None, group=self.superheroes,
                                  lookup=self.lookup, action='save')
        acl3 = ACL.objects.create(user=self.joker, group=None,
                                  lookup=self.lookup, action='kill-rob')

        matched = match_acl(user=self.batman, action='save',
                            model_name='user', app_label='auth')
        self.assertQuerysetEqualsList(matched, [acl1, acl2])

        matched = match_acl(user=self.batman, action='kill-rob',
                            model_name='user', app_label='auth')
        self.assertQuerysetEqualsList(matched, [])

        matched = match_acl(user=self.joker, action='kill-rob',
                            model_name='user', app_label='auth')
        self.assertQuerysetEqualsList(matched, [acl3])
