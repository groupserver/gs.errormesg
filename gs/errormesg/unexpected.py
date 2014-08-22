# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals
import traceback
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
from five import grok
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.core import to_ascii
from .baseerror import BaseError, BaseErrorPage

MESSAGE = '''Hi! I saw a Server Error (500) page when I went to
{url}

I want to see...

--
This technical information may help you fix the error:

{message}
'''

# TODO: Clean up some of the cut-n-paste software engineering.


class UnexpectedError(BaseError, grok.View):
    grok.name('error.html')
    grok.context(Exception)
    index = ZopeTwoPageTemplateFile('browser/templates/error.pt')
    status = 500

    def tracebackMessage(self):
        # obviously this is only going to work if we're *actually* handling
        # an exception
        formatted_tb = traceback.format_exc()
        return formatted_tb.splitlines()[-1].strip()

    def supportMessage(self):
        tracebackMessage = self.tracebackMessage()
        m = MESSAGE.format(url=self.errorUrl, message=tracebackMessage)
        retval = quote(m)
        return retval

    def update(self):
        self.response.setStatus(500)


class UnexpectedZope2(BaseErrorPage):
    '''The Zope2 version of the error page.'''
    status = 500

    def __init__(self, context, request):
        super(UnexpectedZope2, self).__init__(context, request)

        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader(to_ascii('Content-Type'),
                                        to_ascii(contentType))
        self.request.response.setStatus(self.status)  # , lock=True)

    def tracebackMessage(self):
        # obviously this is only going to work if we're *actually* handling
        # an exception
        formatted_tb = traceback.format_exc()
        return formatted_tb.splitlines()[-1].strip()

    def supportMessage(self):
        tracebackMessage = self.tracebackMessage()
        m = MESSAGE.format(url=self.errorUrl, message=tracebackMessage)
        retval = quote(m)
        return retval
