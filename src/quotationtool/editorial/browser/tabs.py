import zope.interface
from z3c.menu.ready2go.item import ContextMenuItem
from zope.publisher.browser import BrowserPage
from zope.traversing.browser.absoluteurl import absoluteURL
import zope.security


class IEditorialStatusTab(zope.interface.Interface):
    pass


class EditorialStatusTab(ContextMenuItem):
    zope.interface.implements(IEditorialStatusTab)


class EditorialStatusTabRedirector(BrowserPage):
    """ Redirects depending on permissions."""

    def __call__(self):
        interaction = zope.security.management.getInteraction()
        canChangeStatus = interaction.checkPermission('quotationtool.editorial.ChangeEditorialStatus', self.context)
        if canChangeStatus:
            self.request.response.redirect(
                absoluteURL(self.context, self.request) 
                + u"/@@changeEditorialStatus.html")
        else:
            self.request.response.redirect(
                absoluteURL(self.context, self.request) 
                + u"/@@revisionHistory.html")
