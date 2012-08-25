# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

import constants
import os
import re
import shutil
import sublime
import sublime_plugin

from Exception import MissingOwnerException

class CopyrightCommand(sublime_plugin.TextCommand):
  '''
  Common functionality for the Auto Copyright command classes.
  '''
  def __init__(self, view):
    '''
    Initializes the CopyrightCommand class.
    '''
    self.settings = sublime.load_settings(constants.SETTINGS_FILE)
    self.view = view

  def format_pattern(self, year, owner):
    text = self.format_text("yyyear", "ooowner")
    text = re.escape(text)
    text = text.replace("yyyear", year)
    pattern = text.replace("ooowner", owner)

    return pattern

  def format_text(self, year, owner):
    '''
    Formats the text of the copyright message.
    '''
    text = self.settings.get(constants.SETTING_COPYRIGHT_MESSAGE)
    text = text.replace("%y", str(year))
    text = text.replace("%o", owner)

    return text    

  def get_owner(self):
    '''
    Gets the copyright owner name that should be used in the copyright message.
    '''
    owner = self.settings.get(constants.SETTING_OWNER)
    if not owner:
      raise MissingOwnerException()

    return owner

  def handle_missing_owner_exception(self):
    '''
    Opens the settings file and suggests the user edit it with the proper owner name.
    '''
    sublime.error_message("Auto Copyright: Default copyright owner not set.  Please edit the settings file to correct this.")
    user_settings_path = os.path.join(sublime.packages_path(), constants.SETTINGS_PATH_USER, constants.SETTINGS_FILE)

    if not os.path.exists(user_settings_path):
      default_settings_path = os.path.join(sublime.packages_path(), constants.PLUGIN_NAME, constants.SETTINGS_FILE)
      shutil.copy(default_settings_path, user_settings_path)

    sublime.active_window().open_file(user_settings_path)
