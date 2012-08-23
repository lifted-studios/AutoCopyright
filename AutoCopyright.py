# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

import comment
import constants
import datetime
import os
import re
import shutil
import sublime
import sublime_plugin

class MissingOwnerException(Exception):
  """
  Exception signifying that the copyright owner information has not been entered into the settings.
  """
  pass

class CopyrightCommand(sublime_plugin.TextCommand):
  """
  Common functionality for the Auto Copyright command classes.
  """
  def __init__(self, view):
    """
    Initializes the UpdateCopyrightCommand class.
    """
    self.settings = sublime.load_settings(constants.SETTINGS_FILE)
    self.view = view

  def format_text(self, year, owner):
    """
    Formats the text of the copyright message.
    """
    text = self.settings.get(constants.SETTING_COPYRIGHT_MESSAGE)
    text = text.replace("%y", str(year))
    text = text.replace("%o", owner)

    return text    

  def get_owner(self):
    """
    Gets the copyright owner name that should be used in the copyright message.
    """
    owner = self.settings.get("owner")
    if not owner:
      raise MissingOwnerException()

    return owner

  def handle_missing_owner_exception(self):
    """
    Opens the settings file and suggests the user edit it with the proper owner name.
    """
    sublime.error_message("Auto Copyright: Copyright owner not set")
    user_settings_path = os.path.join(sublime.packages_path(), constants.SETTINGS_PATH_USER, constants.SETTINGS_FILE)

    if not os.path.exists(user_settings_path):
      default_settings_path = os.path.join(sublime.packages_path(), constants.PLUGIN_NAME, constants.SETTINGS_FILE)
      shutil.copy(default_settings_path, user_settings_path)

    sublime.active_window().open_file(user_settings_path)

class UpdateCopyrightCommand(CopyrightCommand):
  """
  Updates the copyright text, if present.
  """
  def run(self, edit):
    """
    Executes the update command by searching for the copyright text and replacing it, if necessary.
    """
    try:
      self.__update_copyright(edit)

    except MissingOwnerException:
      self.handle_missing_owner_exception()

  def __update_copyright(self, edit):
    """
    Finds the copyright text and replaces it by updating the year if it has changed.
    """
    pattern = self.__format_pattern()
    region = self.__find_pattern(pattern)

    if region:
      oldYear = self.__get_old_year(region, pattern)
      newYear = str(datetime.date.today().year)
      if oldYear != newYear:
        self.__replace_match(edit, region, oldYear, newYear)

  def __format_pattern(self):
    message = self.settings.get(constants.SETTING_COPYRIGHT_MESSAGE)
    message = message.replace("%o", "ooowner")
    message = message.replace("%y", "yyyear")
    message = re.escape(message)
    message = message.replace("ooowner", self.get_owner())
    pattern = message.replace("yyyear", "(\d+)(-\d+)?")

    return pattern

  def __find_pattern(self, pattern):
    return self.view.find(pattern, 0)

  def __get_old_year(self, region, pattern):
    text = self.view.substr(region)
    match = re.match(pattern, text)
    return match.group(1)

  def __replace_match(self, edit, region, oldYear, newYear):
    owner = self.get_owner()
    message = self.format_text(oldYear + "-" + newYear, owner)
    self.view.replace(edit, region, message)

class InsertCopyrightCommand(CopyrightCommand):
  """
  Inserts the copyright text at the top of the file.
  """
  def description(self, *args):
    """
    Describes the command.
    """
    return "Inserts the copyright text at the location of the current selection."

  def run(self, edit):
    """
    Executes the copyright command by inserting the appropriate copyright text at the current selection point.
    """
    try:
      self.__insert_copyright(edit)

    except MissingOwnerException:
      self.__handle_missing_owner_exception()

  def __build_block_comment(self, text):
    """
    Builds a block comment and puts the given text into it.
    """
    self.__get_block_comment_settings()
    endings = self.__get_line_endings()

    def make_comment(line): return self.middleLine + line + endings
    def concatenate(x, y): return x + y

    comment = self.firstLine + endings
    lines = map(make_comment, text.split(endings))
    comment += reduce(concatenate, lines)
    comment += self.lastLine + endings
    return comment

  def __determine_location(self):
    """
    Figures out the right location for the copyright text.
    """
    region = self.view.full_line(0)
    line = self.view.substr(region)
    if re.match("^#!", line):
      return region.end()
    else:
      return 0

  def __get_block_comment_settings(self):
    """
    Determines the appropriate block comment characters for the currently selected syntax.
    """
    lineComments, blockComments = comment.build_comment_data(self.view, 0)
    if len(blockComments) == 0:
      self.firstLine = lineComments[0][0]
      self.middleLine = lineComments[0][0]
      self.lastLine = lineComments[0][0]
    else:
      self.firstLine = blockComments[0][0]
      self.middleLine = ''
      self.lastLine = blockComments[0][1]

  def __get_line_endings(self):
    """
    Gets the appropriate line endings for the view.

    Unix and Mac OS X use the LF character.  Windows uses the CRLF pair.  Old versions of Mac OS used just the CR character.
    """
    if self.view.line_endings() == constants.LINE_ENDING_UNIX:
      return u'\u000a'
    elif self.view.line_endings() == constants.LINE_ENDING_WINDOWS:
      return u'\u000a\u000d'
    else:
      return u'\u000d'

  def __insert_copyright(self, edit):
    """
    Inserts the copyright message into the view.
    """
    year = datetime.date.today().year
    owner = self.get_owner()
    location = self.__determine_location()
    text = self.format_text(year, owner)
    copyrightText = self.__build_block_comment(text)

    self.view.insert(edit, location, copyrightText)
