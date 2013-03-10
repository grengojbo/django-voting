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
from voting.models import Vote
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

#@dajaxice_register(method='GET')
@ensure_csrf_cookie
@dajaxice_register(method='GET', name='voites')
def djax_voites(request, object_id, model, direction='up'):
    lookup_kwargs = {}
    if object_id:
        lookup_kwargs['%s__exact' % model._meta.pk.name] = object_id
    else:
        raise AttributeError('Generic vote view must be called with either '
                             'object_id or slug and slug_field.')
    try:
        obj = model._default_manager.get(**lookup_kwargs)
    except ObjectDoesNotExist:
        raise Http404('No %s found for %s.' %
                      (model._meta.app_label, lookup_kwargs))
    try:
        vote = dict(VOTE_DIRECTIONS)[direction]
    except KeyError:
        raise AttributeError("'%s' is not a valid vote type." % direction)

    try:
        Vote.objects.record_vote(obj, request.user, direction)
    except DuplicateVoteError:
        pass
    res = Vote.objects.get_score(obj)
    dajax.assign('#num_votes{0}'.format(object_id), 'innerHTML', res.num_votes)
    dajax.assign('#score{0}'.format(object_id), 'innerHTML', res.score)
    #dajax.assign('#linkup17', 'innerHTML','<li>iiiiiiiiiiiiiiiiiiiiiiiiiiiiii</li>')

    # try:
    #     ap = AreaPartners.objects.filter(is_public=True)
    #     if f.get('sel_all'):
    #         logger.debug("sel_all: {0}".format(f.get('sel_all')))
    #         if f.get('cat'):
    #             ap = ap.filter(cat=get_cat_slug(f.get('cat')))
    #     elif subcat:
    #         #if f.get('cat'):
    #         #    ap = ap.filter(cat=get_cat_slug(f.get('cat')))
    #         logger.debug("subcat: {0}".format(subcat))
    #         #for sc in subcat:
    #         #    logger.debug("subcat item: {0}".format(sc))
    #         # TODO: переделать на нормальный поиск пока все результаты
    #         ap = ap.filter(category__in=subcat)
    #     #logger.debug("items count: {0}".format(subcat.count()))
    #     render = render_to_string('op/ajax_search.html', {'items': ap})
    #     dajax.assign('#search_res', 'innerHTML', render)
    #     dajax.script('ajax_search_res();')
    # except Exception, e:
    #     logger.debug(e)
    #     dajax.assign('#search_res', 'innerHTML',u'')
    # #a = ap[0]
    return HttpResponse(dajax.json(), mimetype="application/json")

