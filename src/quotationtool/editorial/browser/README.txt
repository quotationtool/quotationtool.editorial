Form for editorial status
-------------------------

>>> import quotationtool.editorial
>>> from zope.configuration.xmlconfig import XMLConfig
>>> XMLConfig('configure.zcml', quotationtool.editorial)()
>>> XMLConfig('configure.zcml', quotationtool.editorial.browser)()

>>> from quotationtool.editorial.browser.status import ChangeEditorialStatus

>>> from quotationtool.editorial.testing import SampleContent, ISampleContent
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
>>> history_pagelet.render()
u'...Compared printed version...'

When accessing the form next time the status should default to the
current status:

>>> changeStatus = ChangeEditorialStatus(foo, TestRequest())
>>> changeStatus.update()
>>> changeStatus.render()
u'...<option id="form-widgets-status-1" value="revised"\n selected="selected">Revised</option>...'


Revision history
----------------

There is also a pagelet that shows the revision history:

>>> from quotationtool.editorial.browser.history import RevisionHistory
>>> revisionHistory = RevisionHistory(foo, TestRequest())
>>> revisionHistory.update()
>>> revisionHistory.render()
u'...<h1>Revision History (reversed order)</h1>...'

We reopen foo again:

>>> request = TestRequest(form={
...     'form.widgets.status': u'reopened',
...	'form.widgets.comment': u'Found a typo',
...	'form.buttons.add': u'Add'}
...	)

>>> changeStatus = ChangeEditorialStatus(foo, request)
>>> changeStatus.update()


Status aware forms
------------------

We can make edit forms for content items aware of the editorial status
of the item. If status is locked, the item should not be
editable. This can easily be achived by mixin in a class that sets the
forms mode property to DISPLAY_MODE (provided the form is based on
z3c.form).

>>> from quotationtool.editorial.browser.form import Z3cFormMixin

So we first create an edit form. Note, that the oder of inheritance is
important.

>>> from z3c.form import form, field
>>> class SampleEditForm(Z3cFormMixin, form.EditForm):
...     fields = field.Fields(ISampleContent)
...

Since its editorial status is unlocked we can edit foo:

>>> editFoo = SampleEditForm(foo, TestRequest())
>>> editFoo.update()
>>> u"<textarea id=\"form-widgets-body\"" in editFoo.render()
True

But if we change status to locked we cannot:

>>> request = TestRequest(form={
...     'form.widgets.status': u'revised',
...	'form.widgets.comment': u'Fixed the typo',
...	'form.buttons.add': u'Add'}
...	)

>>> changeStatus = ChangeEditorialStatus(foo, request)
>>> changeStatus.update()

>>> editFoo = SampleEditForm(foo, TestRequest())
>>> editFoo.update()
>>> u"<textarea id=\"form-widgets-body\"" in editFoo.render()
False


Editorial Status Flag
---------------------

There is also a flag (viewlet) that informs about the editorial
status.

>>> from quotationtool.editorial.browser.flags import EditorialStatusFlag
>>> flag = EditorialStatusFlag(foo, TestRequest(), None, None)
>>> flag.update()
>>> flag.render()
u''

It renders an empty string if status is locked.

But if the item needs a revision or was reopened, it says:

>>> request = TestRequest(form={
...     'form.widgets.status': u'reopened',
...	'form.widgets.comment': u'Found a typo',
...	'form.buttons.add': u'Add'}
...	)
>>> changeStatus = ChangeEditorialStatus(foo, request)
>>> changeStatus.update()

>>> flag = EditorialStatusFlag(foo, TestRequest(), None, None)
>>> flag.update()
>>> flag.render()
u'<abbr title="Editorial Status: Reopened"\n class="editorialstatus">ed</abbr>'


Navigation
----------

There is only one navigation item but a redirector that redirects to
ether the form or the revision history, depending on permissions
granted to the participants in the interaction.

>>> #from quotationtool.editorial.browser.nav import NavItemRedirector
>>> #redirector = NavItemRedirector(foo, TestRequest())
>>> #redirector()
