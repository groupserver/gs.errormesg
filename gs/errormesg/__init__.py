# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
from infrae.wsgi.publisher import *
from zope.publisher.interfaces.browser import IBrowserView
from .baseerror import BaseError  # lint:ok

import logging
log = logging.getLogger('gs.errormesg')
log.info('Monkeypatching infrae.wsgi')


def error(self, error, last_known_obj):
    """Render and log an error.
    """
    # This is the patch ... in the original IBrowserView is IBrowserPage
    if IBrowserView.providedBy(last_known_obj):
        #of the last obj is a view, use it's context (which should be
        # an IAcquirer)
        last_known_obj = last_known_obj.context
    if not IAcquirer.providedBy(last_known_obj):
        last_known_site = getSite()
        if last_known_site is not None:
            last_known_obj = last_known_site
    context = DefaultError(error)
    if IAcquirer.providedBy(last_known_obj):
        context = context.__of__(last_known_obj)
    error_page = queryMultiAdapter(
        (context, self.request), name='error.html')

    if error_page is not None:
        try:
            error_result = error_page()
            if error_result is not None:
                self.response.setBody(error_result)
        except Exception as error:
            log_last_error(
                self.request, self.response, obj=last_known_obj,
                extra="Error while rendering error message")
            self.response.setStatus(500)
            self.response.setBody(ERROR_WHILE_RENDERING_ERROR_TEMPLATE)
    else:
        logger.error('No action defined for last exception')
        self.response.setStatus(500)
        self.response.setBody(DEFAULT_ERROR_TEMPLATE)

WSGIPublication.error = error
