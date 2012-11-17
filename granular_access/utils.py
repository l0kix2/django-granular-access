# coding: utf-8
from __future__ import unicode_literals
from django.core import exceptions
from django.utils.importlib import import_module

def get_function_by_path(path):
    try:
        module_name, function_name = path.rsplit('.', 1)
    except ValueError:
        raise exceptions.ImproperlyConfigured(
            '%s isn\'t a function module_name' % path)
    try:
        module = import_module(module_name)
    except ImportError, e:
        raise exceptions.ImproperlyConfigured(
            'Error importing module_name %s: "%s"' % (module_name, e))
    try:
        function = getattr(module, function_name)
    except AttributeError:
        raise exceptions.ImproperlyConfigured(
            'Module "%s" does not define a "%s" function' % (
                module_name, function_name))
    return function
