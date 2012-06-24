from five import grok
from zope.publisher.interfaces import INotFound
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from urllib import quote

from baseerror import BaseError

class NotFound(grok.View, BaseError):
    grok.name('error.html')
    grok.context(INotFound)
    index = ZopeTwoPageTemplateFile('browser/templates/not_found.pt')

    def update(self):
        self.response.setStatus(404)

    def render(self):
        return self.index(self.context)
        
    def supportMessage(self):
        m = u'''Hi! I saw a Not Found (404) page when I went to
%(url)s

I expected to see...


-----
Technical details:
Code: 404
URL: %(url)s
Referer: %(referer)s
''' % {'url': self.errorUrl,
       'referer': self.refererUrl}

        retval = quote(m)
        
        return retval
