# coding=utf-8
from zope.component import createObject
from Products.Five import BrowserView
from Products.XWFCore.XWFUtils import get_support_email

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

