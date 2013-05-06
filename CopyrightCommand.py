#
# Copyright (c) 2012-2013 by Lifted Studios.  All Rights Reserved.
#

import constants
import helper
import os
import re
import shutil
import sublime
import sublime_plugin


class CopyrightCommand(sublime_plugin.TextCommand):
    """Common functionality for the Auto Copyright command classes."""

    def __init__(self, view):
        """Initializes the CopyrightCommand class."""
        self.settings = sublime.load_settings(constants.SETTINGS_FILE)
        self.view = view
        self.selected_owner = None

    def format_pattern(self, year, owner, fileName):
        """Creates a search pattern for the copyright text."""
        text = self.format_text("yyyear", "ooowner", "fffileName")
        text = re.escape(text)
        text = text.replace("yyyear", year)
        text = text.replace("fffileName", fileName)
        pattern = text.replace("ooowner", owner)

        return pattern

    def format_text(self, year, owner, fileName):
        """Formats the text of the copyright message."""
        if year is None:
            raise TypeError("year cannot be None.")

        if len(owner) == 0:
            raise TypeError("owner cannot be empty.")

        text = self.settings.get(constants.SETTING_COPYRIGHT_MESSAGE)
        text = text.replace("%y", str(year))
        text = text.replace("%o", owner)
        text = text.replace("%f", fileName)

        return text

    def handle_missing_owner_exception(self):
        """Opens the settings file and suggests the user edit it with the proper owner name."""
        fileName = sublime.active_window().active_view().file_name()
        if fileName is not None and fileName.endswith(constants.SETTINGS_FILE):
            return

        helper.error_message(constants.ERROR_MISSING_OWNER)
        user_settings_path = os.path.join(sublime.packages_path(), constants.SETTINGS_PATH_USER)
        user_settings_filename = os.path.join(user_settings_path, constants.SETTINGS_FILE)

        if not os.path.exists(user_settings_path):
            os.makedirs(user_settings_path)

        if not os.path.exists(user_settings_filename):
            default_settings_filename = os.path.join(sublime.packages_path(), constants.PLUGIN_NAME, constants.SETTINGS_FILE)
            shutil.copy(default_settings_filename, user_settings_filename)

        sublime.active_window().open_file(user_settings_filename)
