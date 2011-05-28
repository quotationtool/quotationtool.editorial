import zope.interface
import zope.component
from z3c.pagelet.browser import BrowserPagelet
from zope.authentication.interfaces import IAuthentication
from zope.schema.vocabulary import getVocabularyRegistry

from quotationtool.skin.interfaces import ITabbedContentLayout

from quotationtool.editorial import interfaces


class RevisionHistory(BrowserPagelet):

    zope.interface.implements(ITabbedContentLayout)

    @property
    def history(self):
        return interfaces.IEditorialHistory(self.context)

    def getRevisorTitle(self, id):
        """ Returns the title for the revisor id. Returns the real
        title given in the pau, not the revisor string, which is an
        internal computed value."""
        title = u"Unkown"
        if id is None:
            return title
        pau = zope.component.queryUtility(
            IAuthentication,
            context = self.context
            )
        if pau is not None:
            try:
                title = u""
                for participant in id:
                    title += pau.getPrincipal(id[0]).title + u", "
                if len(title) > 2: 
                    title = title[:-2]
            except Exception:
                pass
        return title

    def getStatusTerm(self, status):
        vocReg = getVocabularyRegistry()
        voc = vocReg.get(self.context, 'quotationtool.editorial.Status')
        return voc.getTermByToken(status)

    
