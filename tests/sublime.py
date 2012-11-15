# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

from MockEdit import MockEdit
from MockSettings import MockSettings
from MockView import MockView
from MockWindow import MockWindow

settings = MockSettings()

def active_window():
  """Returns a mock window."""
  return MockWindow()

def load_settings(file):
  """Simply returns the default mock settings."""
  return settings

