import zope.interface
import zope.component
from z3c.form import field
from z3c.formui import form
from zope.container.interfaces import INameChooser
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from quotationtool.skin.interfaces import ITabbedContentLayout

from quotationtool.editorial import interfaces
from quotationtool.editorial.status import EditorialStatus
from quotationtool.editorial.interfaces import _
from quotationtool.editorial.browser.history import RevisionHistory


class ChangeEditorialStatus(form.AddForm, RevisionHistory):

    zope.interface.implements(ITabbedContentLayout)

    label = _('changeEditorialStatus-label', u"Change Editorial Status")

    fields = field.Fields(interfaces.IEditorialStatus).select('status', 'comment')

    template = ViewPageTemplateFile('changestatus.pt')

    def create(self, data):
        status = EditorialStatus()
        form.applyChanges(self, status, data)
        return status

    def add(self, status):
        history = interfaces.IEditorialHistory(self.context)
        name = INameChooser(history).chooseName(None, status)
        history[name] = status

    def nextURL(self):
        return absoluteURL(self.context, self.request) + u"/@@changeEditorialStatus.html#history"
        

