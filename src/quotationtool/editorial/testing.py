from zope.interface import Interface, implements, classImplements
from zope.annotation.interfaces import IAttributeAnnotatable

from quotationtool.editorial import interfaces



class ISampleContent(Interface):
    pass

class SampleContent(object):
    implements(ISampleContent)

classImplements(SampleContent, interfaces.IHasEditorialStatus)
classImplements(SampleContent, IAttributeAnnotatable)
    
