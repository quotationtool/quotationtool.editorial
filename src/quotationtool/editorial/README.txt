Editorial Status
================

First let's register some components (e.g. vocabulary) via zcml:

>>> import quotationtool.editorial
>>> from zope.configuration.xmlconfig import XMLConfig
>>> XMLConfig('configure.zcml', quotationtool.editorial)()


We need some content which we can do some editorial work on. The
content has must be annotatable because the editorial status and
history is stored as an annotation.

>>> from persistent import Persistent
>>> from zope.annotation.interfaces import IAttributeAnnotatable
>>> import zope.interface
>>> class Foo(Persistent):
...     bar = None
...
>>> zope.interface.classImplements(Foo, IAttributeAnnotatable)

There is a marker interface for which the editorial components are
registered. The only thing we have to do is implementing it on the
content object. (This is typically done via ZCML. We now do it in
python.)

>>> from quotationtool.editorial.interfaces import IHasEditorialStatus
>>> zope.interface.classImplements(Foo, IHasEditorialStatus)

Now, instances of our content class have an editorial history.

>>> foo = Foo()
>>> IHasEditorialStatus.providedBy(foo)
True

>>> from quotationtool.editorial.interfaces import IEditorialHistory
>>> IEditorialHistory(foo)
<quotationtool.editorial.history.EditorialHistory object at ...>

Since the object has not yet been revised, the editorial status is
None and it is not locked.

>>> IEditorialHistory(foo).getCurrentEditorialStatus() is None
True

>>> IEditorialHistory(foo).locked
False

Now let's do a revision of our foo object:

>>> from quotationtool.editorial.status import EditorialStatus
>>> stat1 = EditorialStatus()
>>> stat1.status = 'revised'
>>> stat1.comment = u"1 Dollar, this it is OK"

Revisor and date of revision are set automatically. Revisor is set
from participants in the interaction (see zope.security). So if there
is no one in the interaction revisor will be an empty tuple.

>>> stat1.revisor
()
>>> import datetime
>>> isinstance(stat1.date, datetime.datetime)
True

The revision is stored on the history which is a container that
chooses the name with a namechooser:

>>> from zope.container.interfaces import INameChooser
>>> name = INameChooser(IEditorialHistory(foo)).chooseName(None, stat1)
>>> IEditorialHistory(foo)[name] = stat1
 
>>> len(IEditorialHistory(foo))
1

>>> IEditorialHistory(foo).getCurrentEditorialStatus() == stat1
True

>>> IEditorialHistory(foo).locked
True


OK, now, after some time we have come to think that there is still a
failure in foo:


>>> from quotationtool.editorial.status import EditorialStatus
>>> stat2 = EditorialStatus()
>>> stat2.status = 'reopened'
>>> stat2.comment = u"2 Dollar, this it is not OK"

The revision is again stored on the history which chooses the name
with a namechooser:

>>> from zope.container.interfaces import INameChooser
>>> name = INameChooser(IEditorialHistory(foo)).chooseName(None, stat2)
>>> IEditorialHistory(foo)[name] = stat2
 
>>> len(IEditorialHistory(foo))
2

>>> IEditorialHistory(foo).getCurrentEditorialStatus() == stat2
True

>>> IEditorialHistory(foo).locked
False


The editorial history looks like this:

>>> [status for status in IEditorialHistory(foo).values()] == [stat1, stat2]
True
