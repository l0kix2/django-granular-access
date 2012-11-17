# coding: utf-8
from __future__ import unicode_literals
from django.test import TestCase

class BaseTest(TestCase):
    def assertQuerysetEqualsList(self, queryset, list_):
        self.assertEqual(set(queryset.values_list('id', flat=True)),
                         set(obj.id for obj in list_))
