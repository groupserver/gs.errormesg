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
from urllib import quote
from five import grok
from zope.publisher.interfaces import INotFound
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from .baseerror import BaseError, BaseErrorPage

MESSAGE = '''Hi! I saw a Not Found (404) page when I went to
{url}

I expected to see...

-----
Technical details:
Code: 404
URL: {url}
Referer: {referer}
'''


class NotFound(BaseError, grok.View):
    grok.name('error.html')
    grok.context(INotFound)
    index = ZopeTwoPageTemplateFile('browser/templates/not_found.pt')
    status = 404

    def supportMessage(self):
        m = MESSAGE.format(url=self.errorUrl, referer=self.refererUrl)
        retval = quote(m)
        return retval


class NotFoundZope2(BaseErrorPage):
    '''The Zope2 version of the error page.'''
    status = 404

    def __init__(self, context, request):
        super(NotFoundZope2, self).__init__(context, request)

        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader('Content-Type', contentType)
        self.request.response.setStatus(self.status, lock=True)

    def supportMessage(self):
        m = MESSAGE.format(url=self.errorUrl, referer=self.refererUrl)
        retval = quote(m)
        return retval
