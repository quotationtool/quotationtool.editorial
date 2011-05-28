>>> import quotationtool.editorial
>>> from zope.configuration.xmlconfig import XMLConfig
>>> XMLConfig('configure.zcml', quotationtool.editorial)()
>>> XMLConfig('configure.zcml', quotationtool.editorial.browser)()

>>> from quotationtool.editorial.browser.status import ChangeEditorialStatus

>>> from quotationtool.editorial.testing import SampleContent
>>> root['foo'] = foo = SampleContent()

>>> from quotationtool.editorial.browser.testing import TestRequest 

>>> changeStatus = ChangeEditorialStatus(foo, TestRequest())
>>> changeStatus.update()
>>> isinstance(changeStatus.render(), unicode)
True

>>> request = TestRequest(form={
...     'form.widgets.status': u'revised',
...	'form.widgets.comment': u'Compared printed version with original.',
...	'form.buttons.add': u'Add'}
...	)

>>> changeStatus = ChangeEditorialStatus(foo, request)
>>> changeStatus.update()

>>> from quotationtool.editorial.interfaces import IEditorialHistory
>>> history = IEditorialHistory(foo)
>>> len(history)
1

>>> history.locked
True

>>> history.getCurrentEditorialStatus().comment
u'Compared printed version with original.'

>>> from quotationtool.editorial.browser.history import RevisionHistory
>>> history_pagelet = RevisionHistory(foo, TestRequest())
>>> history_pagelet.update()
>>> #history_pagelet.render()
