#
# Copyright (c) 2012-2013 by Lifted Studios.  All Rights Reserved.
#

import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.dirname(test_dir)
sys.path.append(test_dir)
sys.path.append(source_dir)

import unittest

import comment
import constants
import datetime
import random
import shutil
import sublime

from InsertCopyrightCommand import InsertCopyrightCommand

multiple_owners = [u"Zero", u"One", u"Two", u"Three", u"Four"]


def create_fake_packages_path():
    """Creates a fake packages path and settings file."""

    package_path = os.path.join(sublime.packages_path(), constants.PLUGIN_NAME)
    os.makedirs(package_path)
    shutil.copy(os.path.join(source_dir, constants.SETTINGS_FILE), package_path)


def remove_dir(path):
    """Completely removes the directory and everything in it."""
    for root, dirs, files in os.walk(path, False):
        for name in files:
            os.remove(os.path.join(root, name))

        for dirname in dirs:
            os.rmdir(os.path.join(root, dirname))

    os.rmdir(path)


class TestInsertCopyrightCommand(unittest.TestCase):
    """Tests for the InsertCopyrightCommand class."""

    def setUp(self):
        sublime.settings.set(constants.SETTING_COPYRIGHT_MESSAGE, "|%y|%o|")
        sublime.settings.set(constants.SETTING_PADDING, None)
        self.view = sublime.MockView()
        self.edit = sublime.MockEdit()
        self.command = InsertCopyrightCommand(self.view)
        self.year = datetime.date.today().year
        comment.set_line_comments()

        create_fake_packages_path()

    def tearDown(self):
        if os.path.exists(sublime.packages_path()):
            remove_dir(sublime.packages_path())

    def test_insert_single_owner_with_line_comments_happy_path(self):
        sublime.settings.set(constants.SETTING_OWNERS, u"Lifted Studios")
        self.command.run(self.edit)

        self.assertTrue(self.view.insertCalled)
        self.assertIs(self.edit, self.view.edit)
        self.assertEqual(0, self.view.location)
        self.assertEqual("#\n# |{0}|Lifted Studios|\n#\n".format(self.year), self.view.text)

    def test_insert_single_owner_with_block_comments_happy_path(self):
        comment.set_block_comments()
        sublime.settings.set(constants.SETTING_OWNERS, u"Lifted Studios")
        self.command.run(self.edit)

        self.assertTrue(self.view.insertCalled)
        self.assertIs(self.edit, self.view.edit)
        self.assertEqual(0, self.view.location)
        self.assertEqual("/*\n|{0}|Lifted Studios|\n*/\n".format(self.year), self.view.text)

    def test_insert_line_comments_with_zero_padding(self):
        sublime.settings.set(constants.SETTING_OWNERS, u"Lifted Studios")
        sublime.settings.set(constants.SETTING_PADDING, 0)
        self.command.run(self.edit)

        self.assertTrue(self.view.insertCalled)
        self.assertIs(self.edit, self.view.edit)
        self.assertEqual(0, self.view.location)
        self.assertEqual("# |{0}|Lifted Studios|\n".format(self.year), self.view.text)

    def test_insert_line_comments_with_extra_padding(self):
        sublime.settings.set(constants.SETTING_OWNERS, u"Lifted Studios")
        sublime.settings.set(constants.SETTING_PADDING, 2)
        self.command.run(self.edit)

        self.assertTrue(self.view.insertCalled)
        self.assertIs(self.edit, self.view.edit)
        self.assertEqual(0, self.view.location)
        self.assertEqual("#\n#\n# |{0}|Lifted Studios|\n#\n#\n".format(self.year), self.view.text)

    def test_insert_block_comments_with_zero_padding(self):
        comment.set_block_comments()
        sublime.settings.set(constants.SETTING_OWNERS, u"Lifted Studios")
        sublime.settings.set(constants.SETTING_PADDING, 0)
        self.command.run(self.edit)

        self.assertTrue(self.view.insertCalled)
        self.assertIs(self.edit, self.view.edit)
        self.assertEqual(0, self.view.location)
        self.assertEqual("/* |{0}|Lifted Studios| */\n".format(self.year), self.view.text)

    def test_insert_block_comments_with_extra_padding(self):
        comment.set_block_comments()
        sublime.settings.set(constants.SETTING_OWNERS, u"Lifted Studios")
        sublime.settings.set(constants.SETTING_PADDING, 2)
        self.command.run(self.edit)

        self.assertTrue(self.view.insertCalled)
        self.assertIs(self.edit, self.view.edit)
        self.assertEqual(0, self.view.location)
        self.assertEqual("/*\n\n|{0}|Lifted Studios|\n\n*/\n".format(self.year), self.view.text)

    def test_no_owners(self):
        sublime.settings.set(constants.SETTING_OWNERS, None)
        self.command.run(self.edit)

        user_settings_filename = os.path.join(
                                   sublime.packages_path(),
                                   constants.SETTINGS_PATH_USER,
                                   constants.SETTINGS_FILE)
        self.assertEqual(user_settings_filename, sublime.active_window().opened_file)
        self.assertTrue(os.path.exists(user_settings_filename))

    def test_empty_owners(self):
        sublime.settings.set(constants.SETTING_OWNERS, [])
        self.command.run(self.edit)

        user_settings_filename = os.path.join(
                                   sublime.packages_path(),
                                   constants.SETTINGS_PATH_USER,
                                   constants.SETTINGS_FILE)
        self.assertEqual(user_settings_filename, sublime.active_window().opened_file)
        self.assertTrue(os.path.exists(user_settings_filename))

    def test_insert_multiple_owners_with_line_comments_happy_path(self):
        sublime.settings.set(constants.SETTING_OWNERS, multiple_owners)
        self.command.run(self.edit)

        self.assertEqual(multiple_owners, sublime.active_window().quick_panel_items)
        index = random.randint(0, len(multiple_owners) - 1)
        sublime.active_window().quick_panel_func(index)

        self.assertTrue(self.view.insertCalled)
        self.assertIs(self.edit, self.view.edit)
        self.assertEqual(0, self.view.location)
        self.assertEqual("#\n# |{0}|{1}|\n#\n".format(self.year, multiple_owners[index]), self.view.text)

    def test_insert_multiple_owners_with_block_comments_happy_path(self):
        comment.set_block_comments()
        sublime.settings.set(constants.SETTING_OWNERS, multiple_owners)
        self.command.run(self.edit)

        self.assertEqual(multiple_owners, sublime.active_window().quick_panel_items)
        index = random.randint(0, (len(multiple_owners) - 1))
        sublime.active_window().quick_panel_func(index)

        self.assertTrue(self.view.insertCalled)
        self.assertIs(self.edit, self.view.edit)
        self.assertEqual(0, self.view.location)
        self.assertEqual("/*\n|{0}|{1}|\n*/\n".format(self.year, multiple_owners[index]), self.view.text)

    def test_get_comment_settings_line_comments(self):
        sublime.settings.set(constants.SETTING_LANGUAGES_USE_LINE_COMMENTS, u'Bar')
        sublime.settings.set(u'syntax', u'Packages/Foo/Foo.tmLanguage')
        self.command.get_comment_settings()

        self.assertEqual(u"# ", self.command.firstLine)
        self.assertEqual(u"# ", self.command.middleLine)
        self.assertEqual(u"# ", self.command.lastLine)

    def test_get_comment_settings_block_comments(self):
        comment.set_block_comments()
        sublime.settings.set(constants.SETTING_LANGUAGES_USE_LINE_COMMENTS, u'Bar')
        sublime.settings.set(u'syntax', u'Packages/Foo/Foo.tmLanguage')
        self.command.get_comment_settings()

        self.assertEqual("/*", self.command.firstLine)
        self.assertEqual("", self.command.middleLine)
        self.assertEqual("*/", self.command.lastLine)

    def test_get_comment_settings_block_comments_with_override(self):
        comment.set_block_comments()
        sublime.settings.set(constants.SETTING_LANGUAGES_USE_LINE_COMMENTS, u'Foo')
        sublime.settings.set(u'syntax', u'Packages/Foo/Foo.tmLanguage')
        self.command.get_comment_settings()

        self.assertEqual("// ", self.command.firstLine)
        self.assertEqual("// ", self.command.middleLine)
        self.assertEqual("// ", self.command.lastLine)

    def test_get_comment_settings_no_comment_info(self):
        comment.set_no_comments()
        sublime.settings.set(constants.SETTING_LANGUAGES_USE_LINE_COMMENTS, u'Bar')
        sublime.settings.set(u'syntax', u'Packages/Foo/Foo.tmLanguage')
        self.command.get_comment_settings()

        self.assertEqual("# ", self.command.firstLine)
        self.assertEqual("# ", self.command.middleLine)
        self.assertEqual("# ", self.command.lastLine)

    def test_determine_location_blank_file(self):
        location = self.command.determine_location()

        self.assertEqual(0, location)

    def test_determine_location_with_contents(self):
        self.view.full_line_region = sublime.MockRegion(0, 12)
        self.view.substr_string = u"foo bar baz\n"
        location = self.command.determine_location()

        self.assertEqual(0, location)

    def test_determine_location_with_shebang(self):
        self.view.full_line_region = sublime.MockRegion(0, 12)
        self.view.substr_string = u"#!/bin/bash\n"
        location = self.command.determine_location()

        self.assertEqual(12, location)

if __name__ == "__main__":
    unittest.main()
