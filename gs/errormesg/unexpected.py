# -*- coding: utf-8 *-*
import traceback
from urllib import quote
from five import grok
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from baseerror import BaseError


class UnexpectedError(BaseError, grok.View):
    grok.name('error.html')
    grok.context(Exception)
    index = ZopeTwoPageTemplateFile('browser/templates/error.pt')
    status = 500

    def tracebackMessage(self):
        # obviously this is only going to work if we're *actually* handling an
        # exception
        formatted_tb = traceback.format_exc()
        return formatted_tb.splitlines()[-1].strip()

    def supportMessage(self):
        message = self.tracebackMessage()
        m = u'Hi! I saw a Server Error (500) page when I went to '\
            u'\n%s\n\nI want to see...\n\n--\n\nThis technical '\
            u'information may help you fix the error:\n\n%s' % \
            (self.errorUrl, message)
        retval = quote(m)

        return retval

    def update(self):
        self.response.setStatus(500)

    #def render(self):
    #    return self.index(self.context)
