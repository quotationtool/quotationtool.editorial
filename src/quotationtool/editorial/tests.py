import unittest
import doctest
from zope.component.testing import setUp, tearDown


_flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS


def test_suite():
    return unittest.TestSuite((
            doctest.DocFileSuite('README.txt',
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags = _flags),
            ))
