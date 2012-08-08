# 
# Copyright (c) 2012 Lifted Studios.  All Rights Reserved.
# 

import constants
import datetime
import os
import shutil
import sublime
import sublime_plugin

class MissingOwnerException(Exception):
  """
  Exception signifying that the copyright owner information has not been entered into the settings.
  """
  pass

class InsertCopyrightCommand(sublime_plugin.TextCommand):
  """
  Inserts the copyright text.
  """
  def __init__(self, view):
    """
    Initializes the InsertCopyrightCommand class.
    """
    self.settings = sublime.load_settings(constants.SETTINGS_FILE)
    self.__get_block_comment_settings()
    self.view = view

  def run(self, edit):
    """
    Executes the copyright command by inserting the appropriate copyright text at the current selection point.
    """
    try:
      year = datetime.date.today().year
      
      owner = self.settings.get("owner")
      if not owner:
        raise MissingOwnerException()

      copyrightText = self.__build_block_comment("Copyright (c) {0!s} {1}.  All Rights Reserved.".format(year, owner))
      self.view.replace(edit, self.view.sel()[0], copyrightText)

    except MissingOwnerException:
      sublime.error_message("SublimeCopyright: Copyright owner not set")
      user_settings_path = os.path.join(sublime.packages_path(), 'User', constants.SETTINGS_FILE)

      if not os.path.exists(user_settings_path):
        default_settings_path = os.path.join(sublime.packages_path(), 'SublimeCopyright', constants.SETTINGS_FILE)
        shutil.copy(default_settings_path, user_settings_path)

      sublime.active_window().open_file(user_settings_path)

  def __build_block_comment(self, text):
    """
    Builds a block comment and puts the given text into it.
    """
    if self.view.line_endings() == 'Unix':
      endings = u'\u000a'
    else:
      endings = u'\u000a\u000d'

    def make_comment(line): return self.middleLine + line + endings
    def concatenate(x, y): return x + y

    comment = self.firstLine + endings
    lines = map(make_comment, text.split(endings))
    comment += reduce(concatenate, lines)
    comment += self.lastLine + endings
    return comment

  def __get_block_comment_settings(self):
    """
    Determines the appropriate block comment characters for the currently selected syntax.
    """
    comments = self.settings.get('comments')['Default']
    self.firstLine = comments[0]
    self.middleLine = comments[1]
    self.lastLine = comments[2]
