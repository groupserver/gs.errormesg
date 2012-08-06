from five import grok
from zope.publisher.interfaces import IForbidden
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from urllib import quote

from baseerror import BaseError

class Forbidden(BaseError, grok.View):
    grok.name('forbidden.html')
    grok.context(IForbidden)
    index = ZopeTwoPageTemplateFile('browser/templates/forbidden.pt')
    status = 403

    def supportMessage(self):
        m = u'''Hi! I saw a Forbidden (403) page when I went to
%(url)s

I expected to see...


-----
Technical details:
Code: 403
URL: %(url)s
Referer: %(referer)s
''' % {'url': self.errorUrl,
       'referer': self.refererUrl}

        retval = quote(m)
        
        return retval
