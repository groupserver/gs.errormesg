# coding=utf-8
from urllib import quote
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from baseerror import BaseErrorPage

class Unexpected(BaseErrorPage):
    index = ZopeTwoPageTemplateFile('browser/templates/unexpected.pt')
    def __init__(self, context, request):
        BaseErrorPage.__init__(self, context, request)

        self.requested = request.form.get('q', '')
        self.message = request.form.get('m', '')

    @property
    def supportMessage(self):
        m = u'Hi! I saw an Unexpected Error (500) page when I went to '\
            u'\n%s\n\nI want to see...\n\n--\n\nThis technical '\
            u'information may help you fix the error:\n\n%s' % \
            (self.requested, self.message)
        retval = quote(m)
        return retval
    @property
    def lastMessageLine(self):
        retval = u''
        lines = [e for e in self.message.split('\n') if e.strip()]
        if lines:
            retval = lines[-1]
        return retval
    def __call__(self, *args, **kw):
        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader('Content-Type', contentType)
        self.request.response.setStatus(500, lock=True)
        return self.index(self, *args, **kw)

