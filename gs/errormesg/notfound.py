# coding=utf-8
import re
from urlparse import urlparse
from zope.component import createObject
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class NotFound(BrowserView):
    index = ZopeTwoPageTemplateFile('browser/templates/not_found.pt')
    searchEngines = [
        re.compile('[a-z]*\.?search\.yahoo\.com'),
        re.compile('www.google\.com\.?[a-z]*'),
        re.compile('www.bing.com')
    ]
    # make the template publishable
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.siteInfo = createObject('groupserver.SiteInfo', context)
        self.referer = self.request.get('HTTP_REFERER', '')
        self.refererUrl = urlparse(self.referer)

    @property
    def internalRequest(self):
        siteNetloc = urlparse(self.siteInfo.url).netloc
        retval = self.refererUrl.netloc == siteNetloc
        assert type(retval) == bool
        return retval

    @property
    def searchRequest(self):
        matches = [regexp.match(self.refererUrl.netloc) != None 
                    for regexp in self.serchEngines]
        retval =  reduce(lamda a, b: a or b, matches, False)
        assert type(retval) == bool
        return retval

    @property
    def userRequest(self):
        retval = self.referer == ''
        assert type(retval) == bool
        return retval

    @property
    def externalRequest(self):
        retval = not(self.userRequest or self.searchRequest 
                    or self.internalRequest)
        assert type(retval) == bool
        return retval

    def __call__(self, *args, **kw):
        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader('Content-Type', contentType)
        self.request.response.setStatus(404, lock=True)
        return self.index(self, *args, **kw)

