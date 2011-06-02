from zope.viewlet.viewlet import ViewletBase
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.schema.vocabulary import getVocabularyRegistry
from zope.i18n import translate

from quotationtool.editorial.interfaces import IEditorialHistory, _

class EditorialStatusFlag(ViewletBase):
    """A flag informing about the editorial status.

    It only shows up if unlocked, i.e. editorial work has to be
    done."""

    template = ViewPageTemplateFile('statusflag.pt')

    def locked(self):
        return IEditorialHistory(self.context).locked

    def status(self):
        curr = IEditorialHistory(self.context).getCurrentEditorialStatus()
        vocReg = getVocabularyRegistry()
        voc = vocReg.get(self.context, 'quotationtool.editorial.Status')
        if curr:
            status = curr.status
        else:
            status = 'needs_revision'
        return _('editorial-statusflag-title', 
                 u"Editorial Status: $STATUS",
                 mapping={'STATUS': translate(voc.getTermByToken(status).title, context=self.request)})

    def render(self):
        return self.template()
