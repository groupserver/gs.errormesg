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
from zope.security.interfaces import IForbidden
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from .baseerror import BaseError


class Forbidden(BaseError, grok.View):
    grok.name('error.html')
    grok.context(IForbidden)
    index = ZopeTwoPageTemplateFile('browser/templates/forbidden.pt')
    status = 403

    def supportMessage(self):
        m = '''Hi! I saw a Forbidden (403) page when I went to
%(url)s

I expected to see...


-----
Technical details:
Code: 403
URL: %(url)s
Referer: %(referer)s
''' % {'url': self.errorUrl,
       'referer': self.refererUrl}

        retval = quote(m)
        return retval
