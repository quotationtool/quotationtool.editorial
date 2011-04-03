import zope.interface
from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty
from zope.container.interfaces import IContained
import datetime

from quotationtool.editorial import interfaces


class EditorialStatus(Persistent):
    """An editorial status object, that lives in a history container."""

    zope.interface.implements(interfaces.IEditorialStatus,
                              IContained)

    __name__ = __parent__ = None

    status = FieldProperty(interfaces.IEditorialStatus['status'])
    comment = FieldProperty(interfaces.IEditorialStatus['comment'])
    revisor = FieldProperty(interfaces.IEditorialStatus['revisor'])
    #date = FieldProperty(interfaces.IEditorialStatus['date'])

    def __init__(self):
        self.date = datetime.datetime.now()
