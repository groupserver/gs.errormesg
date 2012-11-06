# -*- coding: utf-8 *-*
import re
from urlparse import urlparse
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.Five import BrowserView
from Products.XWFCore.XWFUtils import get_support_email


class CoreError(object):
    '''The abstract base class for error messages.'''

    status = None  # must be set in subclass

    searchEngines = [
        re.compile('.*search\.yahoo\.com'),
        re.compile('www.google\.com'),
        re.compile('www.bing.com'),
    ]

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
        return retval

    @Lazy
    def supportEmail(self):
        # we pretty much ignore errors. There is bugger all we can do
        # about an error in a error
        try:
            return get_support_email(self.context, self.siteInfo.id)
        except:
            return 'support@'

    @Lazy
    def refererUrl(self):
        # we pretty much ignore errors. There is bugger all we can do
        # about an error in a error
        try:
            return self.context.REQUEST.get('HTTP_REFERER', 'http://#unknown')
        except:
            return 'http://#unknown'

    @Lazy
    def errorUrl(self):
        try:
            return self.context.REQUEST.get('URL', 'http://#unknown')
        except:
            return 'http://#unknown'

    @Lazy
    def internalRequest(self):
        refererHost = urlparse(self.refererUrl)[1]
        siteHost = urlparse(self.errorUrl)[1]
        retval = (refererHost == siteHost) and (not self.directRequest)
        return retval

    @Lazy
    def externalRequest(self):
        retval = (not self.internalRequest) and (not self.directRequest)
        return retval

    @Lazy
    def directRequest(self):
        retval = self.refererUrl in (None, '')
        return retval

    @Lazy
    def searchRequest(self):
        retval = False
        refererHost = urlparse(self.refererUrl)[1]
        for searchEngine in self.searchEngines:
            if searchEngine.match(refererHost):
                retval = True
                break
        return retval

    def supportMessage(self):
        # Should return a support message suitable for email in the subclass.
        raise NotImplementedError


class BaseError(CoreError):
    '''The base error class, that is used by Grok'''

    def update(self):
        self.response.setStatus(self.status)

    def render(self):
        # force the return type to be text/html, just in case
        self.response.setHeader('Content-Type', 'text/html')
        return self.index(self.context)


# This is still used by a couple of things, but relates to the old system
class BaseErrorPage(BrowserView, CoreError):
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        CoreError.__init__(self)
