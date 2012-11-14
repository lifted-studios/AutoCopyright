# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

class MockSettings:
  """Mock settings for Sublime Text."""
  def __init__(self):
    self.settings = {}

  def get(self, name):
    """Gets the named setting."""
    return self.settings[name]

  def set(self, name, value):
    """Sets the named setting."""
    self.settings[name] = value

class MockView:
  """Mock View class for testing."""
  def __init__(self):
    self.insertCalled = False

  def full_line(self, pos):
    return [0, 0]

  def insert(self, edit, location, text):
    self.edit = edit
    self.location = location
    self.text = text
    self.insertCalled = True

  def line_endings(self):
    return 'Unix'

  def substr(self, region):
    return ""

class MockEdit:
  """Mock Edit class for testing."""
  pass

class MockWindow:
  """Mock Window class for testing."""

  def show_quick_panel(self, items, func):
    pass

settings = MockSettings()

def active_window():
  """Returns a mock window."""
  return MockWindow()

def load_settings(file):
  """Simply returns the default mock settings."""
  return settings

