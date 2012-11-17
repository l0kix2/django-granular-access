# coding: utf-8
from __future__ import unicode_literals

from django.test import TestCase

from granular_access.utils import get_function_by_path

def get_groups(user):
    return [1, 2, 3]

class UtilsTest(TestCase):

    FUNCTION_PATH = 'granular_access.tests.utils.get_groups'

    def test_get_function_by_path(self):
        function = get_function_by_path(path=self.FUNCTION_PATH)
        self.assertEqual(
            function({}),
            [1, 2, 3]
        )
