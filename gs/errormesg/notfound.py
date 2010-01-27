# coding=utf-8
import re
from urlparse import urlparse
from urllib import quote
from zope.component import createObject
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class NotFound(BrowserView):
    index = ZopeTwoPageTemplateFile('browser/templates/not_found.pt')
    searchEngines = [
        re.compile('[a-z]*\.?search\.yahoo\.com'),
        re.compile('www.google\.com\.?[a-z]*'),
        re.compile('www.bing.com')
    ]
    internal = 1
    external = 2
    search = 3
    user = 4

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.siteInfo = createObject('groupserver.SiteInfo', context)
        
        self.requested = request.form.get('q', '')
        
        self.referer = request.form.get('r', '')
        #self.referer = self.request.get('HTTP_REFERER', '')
        self.refererUrl = urlparse(self.referer)

        self.__problem = None

    def quote(self, msg):
        assert msg
        retval = quote(mesg)
        assert retval
        return retval

    @property
    def internalRequest(self):
        siteNetloc = urlparse(self.siteInfo.url)[1]
        retval = self.refererUrl[1] == siteNetloc
        assert type(retval) == bool
        return retval

    @property
    def searchRequest(self):
        netloc = self.refererUrl[1]
        matches = [sere.match(netloc) != None 
                   for sere in self.searchEngines]
        retval =  reduce(lambda a, b: a or b, matches, False)
        assert type(retval) == bool
        return retval

    @property
    def userRequest(self):
        retval = self.referer == ''
        assert type(retval) == bool
        return retval

    @property
    def problem(self):
        if self.__problem == None:
            if self.internalRequest:
                self.__problem = internal
            elif self.userRequest:
                self.__problem = user
            elif self.searchRequest:
                self.__problem = search
            else:
                self.__problem = external
        assert self.__problem in (internal, external, search, user)
        return self.__problem
        
    def __call__(self, *args, **kw):
        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader('Content-Type', contentType)
        self.request.response.setStatus(404, lock=True)
        return self.index(self, *args, **kw)

