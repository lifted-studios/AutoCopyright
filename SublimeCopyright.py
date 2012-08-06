import sublime, sublime_plugin

class InsertCopyrightCommand(sublime_plugin.TextCommand):
  """
  Inserts the copyright text.
  """
  def __init__(self, view):
    """
    Initializes the InsertCopyrightCommand class.
    """
    self.copyrightText = "# \n# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.\n# \n"
    self.view = view

  def run(self, edit):
    """
    Executes the copyright command by inserting the appropriate copyright text at the current selection point.
    """
    self.view.replace(edit, self.view.sel()[0], self.copyrightText)
        