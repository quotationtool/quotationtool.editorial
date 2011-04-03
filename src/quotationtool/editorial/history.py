import zope.interface
import zope.component
from zope.container.btree import BTreeContainer
from zope.container.contained import NameChooser
from zope.annotation import factory
from zope.schema.vocabulary import getVocabularyRegistry

from quotationtool.editorial import interfaces


class EditorialHistory(BTreeContainer):
    """The editorial history of a database item. The editorial events
    are stored as editorial status objects in this container. Their
    name is their time of creation.

    """

    zope.interface.implements(interfaces.IEditorialHistory)
    zope.component.adapts(interfaces.IHasEditorialStatus)

    def getCurrentEditorialStatus(self):
        try:
            return self.items()[-1][1]
        except IndexError:
            return None

    @property
    def locked(self):
        cur = self.getCurrentEditorialStatus()
        if cur is None:
            return False
        vocReg = getVocabularyRegistry()
        voc = vocReg.get(cur, 'quotationtool.editorial.Status')
        return voc.getTermByToken(cur.status).locked


editorialHistoryAnnotation = factory(EditorialHistory)


class EditorialStatusNameChooser(NameChooser):
    """ A name chooser for editorial status objects."""

    zope.component.adapts(interfaces.IEditorialHistory)
    
    def chooseName(self, name, obj):
        name = str(obj.date)
        self.checkName(name, obj)
        return name
