import zope.interface
from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty
from zope.container.interfaces import IContained
import datetime
from zope.security.management import queryInteraction

from quotationtool.editorial import interfaces


class EditorialStatus(Persistent):
    """An editorial status object, that lives in a history container."""

    zope.interface.implements(interfaces.IEditorialStatus,
                              IContained)

    __name__ = __parent__ = None

    status = FieldProperty(interfaces.IEditorialStatus['status'])
    comment = FieldProperty(interfaces.IEditorialStatus['comment'])
    revisor = FieldProperty(interfaces.IEditorialStatus['revisor'])
    date = FieldProperty(interfaces.IEditorialStatus['date'])

    def __init__(self):
        # set date
        self.date = datetime.datetime.now()
        # set revisors
        revisor = ()
        interaction = queryInteraction()
        if interaction is not None:
            for participation in interaction.participations:
                if participation.principal is None:
                    continue
                principalid = participation.principal.id
                if not principalid in revisor:
                    revisor = revisor + (unicode(principalid),)
        self.revisor = revisor
