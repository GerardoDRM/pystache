# coding: utf-8

"""
Provides test-related code that can be used by all tests.

"""

import os

import pystache
from pystache import defaults
from pystache.tests import examples

# Save a reference to the original function to avoid recursion.
_DEFAULT_TAG_ESCAPE = defaults.TAG_ESCAPE
_TESTS_DIR = os.path.dirname(pystache.tests.__file__)

DATA_DIR = os.path.join(_TESTS_DIR, 'data')  # i.e. 'pystache/tests/data'.
EXAMPLES_DIR = os.path.dirname(examples.__file__)
# TODO: change SOURCE_DIR to PACKAGE_DIR.
SOURCE_DIR = os.path.dirname(pystache.__file__)
PROJECT_DIR = os.path.join(SOURCE_DIR, '..')
SPEC_TEST_DIR = os.path.join(PROJECT_DIR, 'ext', 'spec', 'specs')


def html_escape(u):
    """
    An html escape function that behaves the same in both Python 2 and 3.

    This function is needed because single quotes are escaped in Python 3
    (to '&#x27;'), but not in Python 2.

    The global defaults.TAG_ESCAPE can be set to this function in the
    setUp() and tearDown() of unittest test cases, for example, for
    consistent test results.

    """
    u = _DEFAULT_TAG_ESCAPE(u)
    return u.replace("'", '&#x27;')


def get_data_path(file_name):
    return os.path.join(DATA_DIR, file_name)


class AssertStringMixin:

    """A unittest.TestCase mixin to check string equality."""

    def assertString(self, actual, expected, format=None):
        """
        Assert that the given strings are equal and have the same type.

        Arguments:

          format: a format string containing a single conversion specifier %s.
            Defaults to "%s".

        """
        if format is None:
            format = "%s"

        # Show both friendly and literal versions.
        details = """String mismatch: %%s\


        Expected: \"""%s\"""
        Actual:   \"""%s\"""

        Expected: %s
        Actual:   %s""" % (expected, actual, repr(expected), repr(actual))

        def make_message(reason):
            description = details % reason
            return format % description

        self.assertEqual(actual, expected, make_message("different characters"))

        reason = "types different: %s != %s (actual)" % (repr(type(expected)), repr(type(actual)))
        self.assertEqual(type(expected), type(actual), make_message(reason))


class AssertIsMixin:

    """A unittest.TestCase mixin adding assertIs()."""

    # unittest.assertIs() is not available until Python 2.7:
    #   http://docs.python.org/library/unittest.html#unittest.TestCase.assertIsNone
    def assertIs(self, first, second):
        self.assertTrue(first is second, msg="%s is not %s" % (repr(first), repr(second)))


class SetupDefaults(object):

    """
    Mix this class in to a unittest.TestCase for standard defaults.

    This class allows for consistent test results across Python 2/3.

    """

    def setup_defaults(self):
        self.original_decode_errors = defaults.DECODE_ERRORS
        self.original_file_encoding = defaults.FILE_ENCODING
        self.original_string_encoding = defaults.STRING_ENCODING

        defaults.DECODE_ERRORS = 'strict'
        defaults.FILE_ENCODING = 'ascii'
        defaults.STRING_ENCODING = 'ascii'

    def teardown_defaults(self):
        defaults.DECODE_ERRORS = self.original_decode_errors
        defaults.FILE_ENCODING = self.original_file_encoding
        defaults.STRING_ENCODING = self.original_string_encoding

