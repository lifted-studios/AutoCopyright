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

  def test_format_text_happy_path(self):
    sublime.settings.set(constants.SETTING_COPYRIGHT_MESSAGE, "%y %o")
    command = CopyrightCommand(None)

    text = command.format_text(1971, "foo")

    self.assertEqual("1971 foo", text)

if __name__ == "__main__":
  unittest.main()
