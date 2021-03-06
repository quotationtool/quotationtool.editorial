import unittest
import doctest
from zope.component.testing import setUp, tearDown
from zope.site.testing import siteSetUp

_flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS


def setUpRoot(test):
    root = siteSetUp(True)
    test.globs['root'] = root


def test_suite():
    return unittest.TestSuite((
            doctest.DocFileSuite('README.txt',
                                 setUp = setUpRoot,
                                 tearDown = tearDown,
                                 optionflags = _flags),
            ))
