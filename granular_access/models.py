# coding: utf-8
from __future__ import unicode_literals

from django.db import models

from .settings import USER_MODEL, GROUP_MODEL
from jsonfield import JSONField

class ModelLookup(models.Model):
    description = models.CharField(
        verbose_name='short description',
        max_length=255,
        blank=True,
    )
    conditions = JSONField(
        verbose_name='filter conditions',
        blank=True, null=True,
    )
    exclusions = JSONField(
        verbose_name='exclude conditions',
        blank=True, null=True,
    )
    content_type = models.ForeignKey(
        verbose_name='content type',
        to='contenttypes.ContentType',
    )

    def __unicode__(self):
        return "[%s] %s" % (self.content_type, self.description)


class ACL(models.Model):
    """Access control list"""
    user = models.ForeignKey(
        to=USER_MODEL,
        verbose_name='user',
        null=True, blank=True,
    )
    group = models.ForeignKey(
        to=GROUP_MODEL,
        verbose_name='Group',
        null=True, blank=True
    )
    lookup = models.ForeignKey(
        to=ModelLookup,
        verbose_name='lookup',
    )
    action = models.SlugField(
        verbose_name='action',
        blank=True,
    )

    def __unicode__(self):
        if self.user is None and self.group is None:
            who = 'everybody'
        elif self.user is not None and self.group is None:
            who = unicode(self.user)
        elif self.user is None and self.group is not None:
            who = unicode(self.group)
        else:
            who = '%s and %s' % (self.user, self.group)

        if self.action:
            what = unicode(self.action)
        else:
            what = 'do anything with'

        objects = unicode(self.lookup)

        return '%s can %s %s' % (who, what, objects)

