# -*- coding: utf-8 *-*
import traceback
from urllib import quote
from five import grok
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from baseerror import BaseError, BaseErrorPage

MESSAGE = u'''Hi! I saw a Server Error (500) page when I went to 
{url}

I want to see...

--
This technical information may help you fix the error:

{message}
'''

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
        self.errorUrl = self.requested = request.form.get('q', '')

        self.traceback = request.form.get('m', '')
        self.tracebackMessage = self.traceback.strip().split('\n')[-1]

        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader('Content-Type', contentType)
        self.request.response.setStatus(self.status, lock=True)
        
    def supportMessage(self):
        m = MESSAGE.format(url=self.requested, message=self.traceback)
        retval = quote(m)
        return retval
