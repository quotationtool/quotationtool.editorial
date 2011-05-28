import zope.publisher
import z3c.form

from quotationtool.skin.interfaces import IQuotationtoolBrowserLayer


class TestRequest(zope.publisher.browser.TestRequest):
    zope.interface.implements(
        z3c.form.interfaces.IFormLayer,
        IQuotationtoolBrowserLayer,
        )
