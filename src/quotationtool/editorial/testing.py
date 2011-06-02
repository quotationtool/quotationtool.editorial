from zope.interface import Interface, implements, classImplements
import zope.schema
from zope.schema.fieldproperty import FieldProperty
from zope.annotation.interfaces import IAttributeAnnotatable

from quotationtool.editorial import interfaces



class ISampleContent(Interface):

    title = zope.schema.TextLine(
        title = u"Title",
        required = True,
        )

    body = zope.schema.Text(
        title = u"Text Body",
        required = True,
        )

class SampleContent(object):
    implements(ISampleContent)

    title = FieldProperty(ISampleContent['title'])
    body = FieldProperty(ISampleContent['body'])


# normally this would be done in ZCML:
classImplements(SampleContent, interfaces.IHasEditorialStatus)
classImplements(SampleContent, IAttributeAnnotatable)
    
