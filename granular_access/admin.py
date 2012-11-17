# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from .models import ACL, ModelLookup

admin.site.register(ACL)
admin.site.register(ModelLookup)
