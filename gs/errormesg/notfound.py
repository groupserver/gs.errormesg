# -*- coding: utf-8 *-*
from urllib import quote
from urlparse import urlparse
from five import grok
from zope.publisher.interfaces import INotFound
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from baseerror import BaseError, BaseErrorPage

MESSAGE = u'''Hi! I saw a Not Found (404) page when I went to
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
