from five import grok
from baseerror import BaseError
from zope.security.interfaces import IForbidden

class Forbidden(grok.View):
    grok.name('error.html')
    grok.context(IForbidden)

    def update(self):
        self.response.setStatus(403)

    def render(self):
        return HTML_TEMPLATE % (
            self.__class__.__name__, str(self.context.error))
