import unittest
import doctest
from zope.component.testing import setUp, tearDown
from zope.site.folder import rootFolder

_flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS


def setUpRoot(test):
    root = rootFolder()
    test.globs['root'] = root


def test_suite():
    return unittest.TestSuite((
            doctest.DocFileSuite('README.txt',
                                 setUp = setUpRoot,
                                 tearDown = tearDown,
                                 optionflags = _flags),
            ))
