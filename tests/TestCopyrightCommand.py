#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.dirname(test_dir)
sys.path.append(test_dir)
sys.path.append(source_dir)

import unittest

import constants
import sublime

from CopyrightCommand import CopyrightCommand


class TestCopyrightCommand(unittest.TestCase):
    """Tests for the CopyrightCommand class."""

    def setUp(self):
        sublime.settings.set(constants.SETTING_COPYRIGHT_MESSAGE, "|%y|%o|")
        self.command = CopyrightCommand(None)

    def test_format_text_happy_path(self):
        text = self.command.format_text(1971, "foo")

        self.assertEqual("|1971|foo|", text)

    def test_format_text_will_accept_string_for_year(self):
        text = self.command.format_text("1971", "foo")

        self.assertEqual("|1971|foo|", text)

    def test_format_text_raises_on_missing_year(self):
        with self.assertRaises(TypeError):
            self.command.format_text(None, "foo")

    def test_format_text_raises_on_missing_owner(self):
        with self.assertRaises(TypeError):
            self.command.format_text(1971, None)

    def test_format_text_raises_on_empty_owner(self):
        with self.assertRaises(TypeError):
            self.command.format_text(1971, "")

    def test_format_pattern_happy_path(self):
        text = self.command.format_pattern("(\d+)(-\d+)?", "foo")

        self.assertEqual("\\|(\d+)(-\d+)?\\|foo\\|", text)

    def test_format_pattern_raises_on_missing_year(self):
        with self.assertRaises(TypeError):
            self.command.format_pattern(None, "foo")

    def test_format_pattern_raises_on_missing_owner(self):
        with self.assertRaises(TypeError):
            self.command.format_pattern("(\d+)(-\d+)?", None)

if __name__ == "__main__":
    unittest.main()
