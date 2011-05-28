from z3c.form.interfaces import DISPLAY_MODE, INPUT_MODE
from zope.schema.vocabulary import getVocabularyRegistry

from quotationtool.editorial import interfaces
from quotationtool.editorial.interfaces import _


class Z3cFormMixin(object):
    """A mixin class for z3c.form or z3c.formui forms. Depending on
    editorial status it set the form's mode to DISPLAY_MODE so that
    the item cannot be edited any more. In that case it also sets the
    status message."""

    @property
    def mode(self):
        history = interfaces.IEditorialHistory(self.getContent())
        if history.locked:
            # we also use this as a hook to set the status message
            vocReg = getVocabularyRegistry()
            voc = vocReg.get(self.getContent(), 'quotationtool.editorial.Status')
            status = voc.getTermByToken(history.getCurrentEditorialStatus().status)
            self.status = _('editorialstatus-formmessage', 
                            u"Editorial status: $TITLE - $DESCRIPTION",
                            mapping={'TITLE': status.title, 
                                     'DESCRIPTION': status.description}
                            )
            # set display mode
            return DISPLAY_MODE
        else:
            return INPUT_MODE


    
