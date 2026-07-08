# (C) Copyright 2020-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import datetime
import unittest
from unittest import mock

from flake8_ets.copyright_header import (
    BadCopyrightEndYearError,
    copyright_header,
    end_year_from_string,
    MissingCopyrightHeaderError,
)


class TestCopyrightHeader(unittest.TestCase):
    def test_good_copyright(self):
        file_contents = """\
# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
        lines = file_contents.splitlines(keepends=True)
        errors = list(copyright_header(lines, end_year=2020))
        self.assertEqual(len(errors), 0)

    def test_empty_file(self):
        file_contents = ""
        lines = file_contents.splitlines(keepends=True)
        errors = list(copyright_header(lines, end_year=2020))
        self.assertEqual(len(errors), 0)

    def test_missing_copyright(self):
        file_contents = """\
# This Python file doesn't start with a copyright statement.

import math

x = math.sqrt(1729)
"""
        lines = file_contents.splitlines(keepends=True)
        errors = list(copyright_header(lines, end_year=2020))
        self.assertEqual(len(errors), 1)
        error = errors[0]
        self.assertIsInstance(error, MissingCopyrightHeaderError)
        self.assertEqual(error.lineno, 1)
        self.assertEqual(error.col_offset, 0)
        self.assertTrue(
            error.full_message.startswith(MissingCopyrightHeaderError.code)
        )
        self.assertIn(
            "header is missing, or doesn't match", error.full_message
        )

    def test_well_formed_copyright_with_wrong_end_year(self):
        file_contents = """\
# (C) Copyright 2005-2010 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
        lines = file_contents.splitlines(keepends=True)
        errors = list(copyright_header(lines, end_year=2020))
        self.assertEqual(len(errors), 1)
        error = errors[0]
        self.assertIsInstance(error, BadCopyrightEndYearError)
        self.assertEqual(error.lineno, 1)
        self.assertEqual(error.col_offset, 16)
        self.assertTrue(
            error.full_message.startswith(BadCopyrightEndYearError.code)
        )
        self.assertIn("end year (2010) should be 2020", error.full_message)


class TestEndYearFromString(unittest.TestCase):
    def test_explicit_year(self):
        self.assertEqual(end_year_from_string("2020"), 2020)

    def test_current(self):
        # Patch the clock so the result is deterministic even if the test
        # happens to run across a year boundary.
        with mock.patch("flake8_ets.copyright_header.datetime") as mock_dt:
            mock_dt.datetime.today.return_value = datetime.datetime(2023, 6, 1)
            self.assertEqual(end_year_from_string("current"), 2023)

    def test_invalid_value(self):
        with self.assertRaises(ValueError) as cm:
            end_year_from_string("not-a-year")
        # The message should mention the accepted values.
        self.assertIn("current", str(cm.exception))
        self.assertIn("not-a-year", str(cm.exception))
