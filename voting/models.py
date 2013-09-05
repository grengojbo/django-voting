# -*- mode: python; coding: utf-8; -*-
from datetime import datetime
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

from voting.managers import VoteManager


SCORES = (
    (+1, u'+1'),
    (-1, u'-1'),
)


class Vote(models.Model):
    """
    A vote on an object by a User.
    """
    #user = models.ForeignKey(User, related_name='user', blank=True, null=True)
    sessions_hash = models.CharField(_(u'Sessions'), max_length=255, blank=True, null=True)
    model_view = models.CharField(_(u'Model View'), max_length=255)
    object_id = models.PositiveIntegerField()
    vote = models.SmallIntegerField(choices=SCORES)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    last_update = models.DateTimeField(editable=False, auto_now=True)

    objects = VoteManager()

    class Meta:
        db_table = 'votes'
        # One vote per user per object
        #unique_together = (('user', 'content_type', 'object_id'),)
        unique_together = (('sessions_hash', 'model_view', 'object_id'),)

    def __unicode__(self):
        return u'{0}: {1} on {2}'.format(self.user, self.vote, self.model_view)

    def is_upvote(self):
        return self.vote == 1

    def is_downvote(self):
        return self.vote == -1


class ViewsObj(models.Model):
    #user = models.ForeignKey(User, related_name='user', blank=True, null=True)
    #sessions = models.CharField(_(u'Sessions'), blank=True, null=True)
    model_view = models.CharField(_(u'Model View'), max_length=255)
    object_id = models.PositiveIntegerField()
    views = models.PositiveIntegerField(_(u'views'), default=0)
    last_update = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        db_table = 'votes_view'
        unique_together = (('model_view', 'object_id'),)

    def __unicode__(self):
        return u'{0}: {1}'.format(self.model_view, self.views)
