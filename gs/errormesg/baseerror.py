# coding=utf-8
from zope.component import createObject
from Products.Five import BrowserView
from Products.XWFCore.XWFUtils import get_support_email

from urlparse import urlparse
import re

class BaseError(object):
    searchEngines = [
        re.compile('.*search\.yahoo\.com'),
        re.compile('www.google\.com'),
        re.compile('www.bing.com'),
    ]
    # must be set in subclass
    status = None 
    
    @property
    def siteInfo(self):
        siteInfo = createObject('groupserver.SiteInfo',
                                self.context)
        return siteInfo

    @property
    def supportEmail(self):
        return get_support_email(self.context, self.siteInfo.id)

    @property
    def refererUrl(self):
        return self.context.REQUEST.get('HTTP_REFERER', None)

    @property
    def errorUrl(self):
        return self.context.REQUEST['URL']

    @property
    def internalRequest(self):
        refererHost = urlparse(self.refererUrl)[1]
        siteHost = urlparse(self.errorUrl)[1]
        retval = (refererHost == siteHost) and (not self.directRequest)

        return retval
    
    @property 
    def externalRequest(self):
        retval = (not self.internalRequest) and (not self.directRequest)

        return retval

    @property
    def directRequest(self):
        retval = self.refererUrl in (None, '')       
        
        return retval

    @property
    def searchRequest(self):
        retval = False
        refererHost = urlparse(self.refererUrl)[1]
        for searchEngine in self.searchEngines:
            if searchEngine.match(refererHost):
                retval = True
                break
        return retval

    def update(self):
        self.response.setStatus(self.status)

    def supportMessage(self):
        # Should return a support message suitable for email in the subclass.
        raise NotImplementedError

    def render(self):
        # force the return type to be text/html, just in case
        self.response.setHeader('Content-Type', 'text/html')
        return self.index(self.context)


# This is still used by a couple of things, but relates to the old system
class BaseErrorPage(BrowserView):
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.__siteInfo = self.__supportEmail = None
    
    @property
    def siteInfo(self):
        if self.__siteInfo == None:
            self.__siteInfo = createObject('groupserver.SiteInfo',
                self.context)
        return self.__siteInfo

    @property
    def supportEmail(self):
        if self.__supportEmail == None:
            self.__supportEmail = get_support_email(self.context,
                                    self.siteInfo.id)
        return self.__supportEmail
