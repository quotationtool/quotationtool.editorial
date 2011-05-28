import zope.interface
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from quotationtool.editorial import interfaces
from quotationtool.editorial.interfaces import _


status = {
    'needs_revision' : (_('status-needsrevision-title',
                          u"Needs Revision"),
                        _('status-needsrevision-desc',
                         u"The item was not yet revised."),
                        False,
                        ),
    'revised' : (_('status-revised-title',
                   u"Revised"),
                 _('status-revised-desc', 
                   u"The item was editorialy revised and corrected. It is now locked for editing."),
                 True,
                 ),
    'reopened' : (_('status-reopened-title',
                    u"Reopened"),
                  _('status-reopened-desc',
                    u"The item was revised and locked already but errors were still found. It is thus reopened for editing."),
                  False,
                  ),
    }


class StatusTerm(SimpleTerm):

    zope.interface.implements(interfaces.IStatusTerm)

    def __init__(self, token, title = u"", description = u"", locked = False):
        self.token = self.value = token
        self.title = title
        self.description = description
        self.locked = locked


def StatusVocabulary(context):
    terms = []
    for key in ('needs_revision', 'revised', 'reopened'):
        value = status[key]
        terms.append(StatusTerm(key,
                                title = value[0],
                                description = value[1],
                                locked = value[2],
                                ))
    return SimpleVocabulary(terms)
                     
zope.interface.alsoProvides(StatusVocabulary, IVocabularyFactory)
