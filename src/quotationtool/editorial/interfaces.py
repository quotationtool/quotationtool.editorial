import zope.interface
import zope.schema
from zope.container.interfaces import IContainer
from zope.container.constraints import contains
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import ITitledTokenizedTerm


_ = MessageFactory('quotationtool')


class IHasEditorialStatus(zope.interface.Interface):
    """A marker interface for objects that have an editorial status.

    There are some components that are registered for objects that
    implement this marker interface:

    1) adapter to IEditorialHistory

    2) view components that let you do editorial jobs (setting status
    and writing a comment about what you invested in revising the
    object).

    There is also a mixin class that makes it easy to lock the object
    or not depending on the status.

    """


class IStatusTerm(ITitledTokenizedTerm):

    description = zope.schema.TextLine(
        title = u"Description",
        description = u"The description of the term.",
        required = True,
        )

    locked = zope.schema.Bool(
        title = u"Locked",
        description = u"If True, then the item must not be edited.",
        required = False,
        )


def validComment(comment):
    return len(comment) > 10


class IEditorialStatus(zope.interface.Interface):
    """The editorial status of a database item is an object that holds
    its status and a comment about the editorial work invested. It
    also stored the date (datetime) of the revision and the ID of the
    user how did the revision.

    This is not an adapter.
    """

    status = zope.schema.Choice(
        title = _('ieditorialstatus-status-title',
                  u"Status"),
        description = _('ieditorialstatus-status-desc',
                        u"The editorial status of this database item."),
        vocabulary = 'quotationtool.editorial.Status',
        default = 'needs_revision',
        required = True,
        )

    comment = zope.schema.Text(
        title = _('ieditorialstatus-comment-title',
                  u"Comment"),
        description = _('ieditorialstatus-comment-desc',
                        u"Please write a short description of the editorial work you invested on this item."),
        required = True,
        constraint = validComment,
        )

    date = zope.schema.Datetime(
        title = u"Date",
        description = u"Datetime of last editorial revision. This is set automatically.",
        readonly = True,
        required = True,
        )

    revisor = zope.schema.TextLine(
        title = u"Revisor",
        description = u"The user ID of the last revisor. This is set automatically.",
        readonly = True,
        required = True,
        )
        

class IEditorialHistory(IContainer):
    """A container that stores outdated editorial status objects.

    

    The __name__ of an editorial status object should be the datetime
    of the revision.

    This an adapter.
    """

    contains(IEditorialStatus)

    def getCurrentEditorialStatus():
        """ Returns the current editorial status, i.e. the editorial status."""

    locked = zope.interface.Attribute("""True if item is locked for editing, else False.""")
