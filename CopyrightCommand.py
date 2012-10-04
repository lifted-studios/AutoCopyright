# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

import constants
import helper
import os
import re
import shutil
import sublime
import sublime_plugin

from Exception import MissingOwnerException

class CopyrightCommand(sublime_plugin.TextCommand):
  """Common functionality for the Auto Copyright command classes."""

  def __init__(self, view):
    """Initializes the CopyrightCommand class."""
    self.settings = sublime.load_settings(constants.SETTINGS_FILE)
    self.view = view
    self.selected_owner = None

  def format_pattern(self, year, owner):
    """Creates a search pattern for the copyright text."""
    text = self.format_text("yyyear", "ooowner")
    text = re.escape(text)
    text = text.replace("yyyear", year)
    pattern = text.replace("ooowner", owner)

    return pattern

  def format_text(self, year, owner):
    """Formats the text of the copyright message."""
    text = self.settings.get(constants.SETTING_COPYRIGHT_MESSAGE)
    text = text.replace("%y", str(year))
    text = text.replace("%o", owner)

    return text    

  def handle_missing_owner_exception(self):
    """Opens the settings file and suggests the user edit it with the proper owner name."""
    helper.error_message(constants.ERROR_MISSING_OWNER)
    user_settings_path = os.path.join(sublime.packages_path(), constants.SETTINGS_PATH_USER, constants.SETTINGS_FILE)

    if not os.path.exists(user_settings_path):
      default_settings_path = os.path.join(sublime.packages_path(), constants.PLUGIN_NAME, constants.SETTINGS_FILE)
      shutil.copy(default_settings_path, user_settings_path)

    sublime.active_window().open_file(user_settings_path)
