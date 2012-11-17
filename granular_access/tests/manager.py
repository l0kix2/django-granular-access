# coding: utf-8
from __future__ import unicode_literals

from django.db.models.query import QuerySet
from django.contrib.auth.models import User, UserManager
from django.test.utils import override_settings

from .base import BaseTest
from granular_access.queryset import AccessQuerySet, AccessQuerySetMixin
from granular_access.manager import AccessManager, AccessManagerMixin

class AccessQuerySetTest(BaseTest):
    def setUp(self):
        self.batman = User.objects.create_user(username='batman',
                                               email='batman@gotham.us')

    def test_queryset(self):
        queryset = AccessQuerySet(model=User)

        filtered = queryset.available(to=self.batman, action='edit')

        self.assertQuerysetEqualsList(
            filtered, []
        )

    @override_settings(CONSIDER_SUPERUSER=True)
    def test_queryset_superuser_enabled(self):
        self.batman.is_superuser = True
        self.batman.save()

        queryset = AccessQuerySet(model=User)

        filtered = queryset.available(to=self.batman, action='edit')

        self.assertQuerysetEqualsList(
            filtered, [self.batman]
        )

class AccessQuerySetMixinTest(BaseTest):
    class MyCustomQuerySet(QuerySet, AccessQuerySetMixin):
        pass

    def setUp(self):
        self.batman = User.objects.create_user(username='batman',
                                               email='batman@gotham.us')

    def test_queryset_mixin(self):
        queryset = self.MyCustomQuerySet(model=User)

        filtered = queryset.available(to=self.batman, action='edit')

        self.assertQuerysetEqualsList(
            filtered, []
        )

    @override_settings(CONSIDER_SUPERUSER=True)
    def test_queryset_mixin_superuser_enabled(self):
        self.batman.is_superuser = True
        self.batman.save()

        queryset = self.MyCustomQuerySet(model=User)

        filtered = queryset.available(to=self.batman, action='edit')

        self.assertQuerysetEqualsList(
            filtered, [self.batman]
        )

class AccessManangerTest(BaseTest):
    class UserAccessProxy(User):
        objects = AccessManager()
        class Meta:
            proxy = True

    def setUp(self):
        self.batman = User.objects.create_user(username='batman',
                                               email='batman@gotham.us')

    def test_manager(self):
        filtered = self.UserAccessProxy.objects.available(
            to=self.batman, action='edit')

        self.assertQuerysetEqualsList(
            filtered, []
        )

    @override_settings(CONSIDER_SUPERUSER=True)
    def test_manager_superuser_enabled(self):
        self.batman.is_superuser = True
        self.batman.save()

        filtered = self.UserAccessProxy.objects.available(
            to=self.batman, action='edit')

        self.assertQuerysetEqualsList(
            filtered, [self.batman]
        )

class AccessManangerMixinTest(BaseTest):

    class UserAccessProxy(User):
        class MyCustomAccessManager(UserManager, AccessManagerMixin):
            pass

        objects = MyCustomAccessManager()
        class Meta:
            proxy = True

    def setUp(self):
        self.batman = User.objects.create_user(username='batman',
                                               email='batman@gotham.us')

    def test_manager(self):
        filtered = self.UserAccessProxy.objects.available(
            to=self.batman, action='edit')

        self.assertQuerysetEqualsList(
            filtered, []
        )

    @override_settings(CONSIDER_SUPERUSER=True)
    def test_manager_superuser_enabled(self):
        self.batman.is_superuser = True
        self.batman.save()

        filtered = self.UserAccessProxy.objects.available(
            to=self.batman, action='edit')

        self.assertQuerysetEqualsList(
            filtered, [self.batman]
        )
