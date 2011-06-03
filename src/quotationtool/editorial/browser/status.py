import zope.interface
import zope.component
from z3c.form import field
from z3c.formui import form
from zope.container.interfaces import INameChooser
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
import zc.resourcelibrary

from quotationtool.skin.interfaces import ITabbedContentLayout

from quotationtool.editorial import interfaces
from quotationtool.editorial.status import EditorialStatus
from quotationtool.editorial.interfaces import _
from quotationtool.editorial.browser.history import RevisionHistory


class ChangeEditorialStatus(form.AddForm, RevisionHistory):

    zope.interface.implements(ITabbedContentLayout)

    label = _('changeEditorialStatus-label', u"Change Editorial Status")

    info = _('changeEditorialStatus-info', 
             u"Set the editorial state and write a short description of the editorial work you invested on this item. <br />For a history of editorial revisions see below.")

    fields = field.Fields(interfaces.IEditorialStatus).select('status', 'comment')

    template = ViewPageTemplateFile('changestatus.pt')

    def __init__(self, context, request):
        super(ChangeEditorialStatus, self).__init__(context, request)
        zc.resourcelibrary.need('quotationtool.editorial')

    def updateWidgets(self):
        super(ChangeEditorialStatus, self).updateWidgets()
        current_status = interfaces.IEditorialHistory(self.getContent()).getCurrentEditorialStatus()
        if current_status:
            self.widgets['status'].value = (current_status.status,)

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
        

