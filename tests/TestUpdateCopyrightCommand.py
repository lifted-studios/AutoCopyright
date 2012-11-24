#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.dirname(test_dir)
sys.path.append(test_dir)
sys.path.append(source_dir)

import constants
import unittest
import sublime

from MockEdit import MockEdit
from MockView import MockView
from UpdateCopyrightCommand import UpdateCopyrightCommand

test_copyright = u"#\n# Copyright (c) 2010 by Lifted Studios.  All Rights Reserved.\n#\n"


class TestUpdateCopyrightCommand(unittest.TestCase):
    def setUp(self):
        self.edit = MockEdit()
        self.view = MockView(test_copyright)
        self.command = UpdateCopyrightCommand(self.view)

    def test_update_single_owner_happy_path(self):
        sublime.settings.set(constants.SETTING_OWNERS, u"Lifted Studios")
        self.command.run(self.edit)

    def test_get_owners_single_owner(self):
        sublime.settings.set(constants.SETTING_OWNERS, u"Lifted Studios")
        owners = self.command.get_owners()

        self.assertEqual([u"Lifted Studios"], owners)

    def test_get_owners_single_owner_in_array(self):
        sublime.settings.set(constants.SETTING_OWNERS, [u"Lifted Studios"])
        owners = self.command.get_owners()

        self.assertEqual([u"Lifted Studios"], owners)

    def test_get_owners_multiple_owners(self):
        sublime.settings.set(constants.SETTING_OWNERS, [u"Lifted Studios", u"FooBar Industries"])
        owners = self.command.get_owners()

        self.assertEqual([u"Lifted Studios", u"FooBar Industries"], owners)
