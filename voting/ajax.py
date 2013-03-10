# -*- mode: python; coding: utf-8; -*-
#import simplejson
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from op.views import get_cat_slug
from django.db.models import Q
from userena.utils import signin_redirect, get_profile_model
from userena import signals as userena_signals
from django.core.urlresolvers import reverse
from userena import settings as userena_settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from userena.decorators import secure_required
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .models import AreaPartners
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

#@dajaxice_register(method='GET')
#@ensure_csrf_cookie
@dajaxice_register(method='POST', name='voites')
def djax_voites(request, form, success_url=None):
    #f = deserialize_form(form)
    #logger.debug("lot_form: {0}".format(f))
    # subcat = f.getlist('subcat')
    # if subcat:
    #     logger.debug("subcat: {0}".format(subcat))
    # #logger.debug("subcat: {0}".format(subcat))
    dajax = Dajax()
    # #signup_form = SignupForm
    # #if userena_settings.USERENA_WITHOUT_USERNAMES:
    # #    signup_form = SignupFormOnlyEmail
    #
    # #form = signup_form(deserialize_form(form))
    #
    # #dajax.alert("Form is_valid(), your username is: %s" % form.cleaned_data.get('username'))
    dajax.assign('#linkup17', 'innerHTML','<li>iiiiiiiiiiiiiiiiiiiiiiiiiiiiii</li>')
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

