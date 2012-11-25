# coding: utf-8
from __future__ import unicode_literals

from django.db import models

from .settings import USER_MODEL, GROUP_MODEL

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
        to='stored_filters.Filter',
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

