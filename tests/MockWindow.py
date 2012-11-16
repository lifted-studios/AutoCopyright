# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

class MockWindow:
  """Mock Window class for testing."""

  def open_file(self, path):
    self.opened_file = path

  def show_quick_panel(self, items, func):
    pass
