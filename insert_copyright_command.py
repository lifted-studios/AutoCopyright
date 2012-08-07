# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

import datetime
import sublime
import sublime_plugin

class InsertCopyrightCommand(sublime_plugin.TextCommand):
  """
  Inserts the copyright text.
  """
  def __init__(self, view):
    """
    Initializes the InsertCopyrightCommand class.
    """
    self.__get_block_comment_settings()
    self.view = view

  def run(self, edit):
    """
    Executes the copyright command by inserting the appropriate copyright text at the current selection point.
    """
    year = datetime.date.today().year
    copyrightText = self.__build_block_comment("Copyright (c) {0} by Lifted Studios.  All Rights Reserved." % (year))
    self.view.replace(edit, self.view.sel()[0], copyrightText)

  def __build_block_comment(self, text):
    """
    Builds a block comment and puts the given text into it.
    """
    def make_comment(line): return self.middleLine + line + "\n"
    def concatenate(x, y): return x + y

    comment = self.firstLine + "\n"
    lines = map(make_comment, text.split("\n"))
    comment += reduce(concatenate, lines)
    comment += self.lastLine + "\n"
    return comment

  def __get_block_comment_settings(self):
    """
    Determines the appropriate block comment characters for the currently selected syntax.
    """
    self.firstLine = "# "
    self.middleLine = "# "
    self.lastLine = "# "
