# -*- mode: python; coding: utf-8; -*-
#import simplejson
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from op.views import get_cat_slug
from django.db.models import Q
#from userena.utils import signin_redirect, get_profile_model
#from userena import signals as userena_signals
from django.core.urlresolvers import reverse
#from userena import settings as userena_settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
#from userena.decorators import secure_required
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_model
from voting.managers import DuplicateVoteError
from django.http import Http404
from voting.models import Vote, ViewsObj
from django.db.models import F
#@secure_required
#@csrf_exempt

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class ErrorList(list):
    """
    A collection of errors that knows how to display itself in various formats.
    """
    def __unicode__(self):
        return self.as_ul()

    def as_ul(self):
        if not self: return u''

VOTE_DIRECTIONS = (('up', 1), ('down', -1), ('clear', 0))

@dajaxice_register(method='GET', name='jboVote')
def djax_views(request, items, model):
    dajax = Dajax()
    res = Vote.objects.get_scores_in_bulk(items, model)
    for r in res:
        dajax.assign('#num_votes{0}'.format(r['object_id']), 'innerHTML', r['num_votes'])
        dajax.assign('#score{0}'.format(r['object_id']), 'innerHTML', r['score'])
    viewDisable = Vote.objects.filter(object_id__in=items, model_view=model, sessions_hash=request.session)
    for v in viewDisable:
        dajax.add_css_class('#vote-{0}'.format(v.pk), 'disabled')
    return HttpResponse(dajax.json(), mimetype="application/json")

@dajaxice_register(method='GET', name='jboviews')
def djax_views(request, items, model):
    dajax = Dajax()
    for item in items:
        o, c = ViewsObj.objects.get_or_create(model_view=model, object_id=item)
        o.views += 1
        o.save()
        dajax.assign('#num-view-{0}'.format(item), 'innerHTML', o.views)
    return HttpResponse(dajax.json(), mimetype="application/json")

#@dajaxice_register(method='GET')
@ensure_csrf_cookie
@dajaxice_register(method='GET', name='voites')
def djax_voites(request, object_id, model, direction='up'):
    dajax = Dajax()

    try:
        vote = dict(VOTE_DIRECTIONS)[direction]
    except KeyError:
        raise AttributeError("'%s' is not a valid vote type." % direction)

    try:
        Vote.objects.record_vote(object_id, model, request.user, request.session, vote)
    except DuplicateVoteError:
        pass
    res = Vote.objects.get_score(object_id, model)
    dajax.assign('#num_votes{0}'.format(object_id), 'innerHTML', res['num_votes'])
    #logger.error('AAA {0}'.format(request.user.username))
    #dajax.assign('#num_votes{0}'.format(object_id), 'innerHTML', request.user.username)
    dajax.assign('#score{0}'.format(object_id), 'innerHTML', res['score'])
    return HttpResponse(dajax.json(), mimetype="application/json")

