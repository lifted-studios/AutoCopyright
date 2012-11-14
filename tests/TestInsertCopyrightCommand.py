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
import datetime
import sublime

from InsertCopyrightCommand import InsertCopyrightCommand

class TestInsertCopyrightCommand(unittest.TestCase):
  """Tests for the InsertCopyrightCommand class."""

  def setUp(self):
    sublime.settings.set(constants.SETTING_COPYRIGHT_MESSAGE, "|%y|%o|")
    self.view = sublime.MockView()
    self.edit = sublime.MockEdit()
    self.command = InsertCopyrightCommand(self.view)

  def test_insert_single_owner_happy_path(self):
    sublime.settings.set(constants.SETTING_OWNERS, u"Lifted Studios")
    self.command.run(self.edit)

    self.assertTrue(self.view.insertCalled)

if __name__ == "__main__":
  unittest.main()
