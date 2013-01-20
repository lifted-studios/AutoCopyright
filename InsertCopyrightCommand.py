#
# Copyright (c) 2012-2013 by Lifted Studios.  All Rights Reserved.
#

import os
import sys

# Required so that the comment module can be imported reliably on startup
package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
default_package_dir = os.path.join(package_dir, 'Default')
sys.path.append(default_package_dir)

import comment
import constants
import datetime
import re
import sublime

from CopyrightCommand import CopyrightCommand
from Exception import MissingOwnerException


class InsertCopyrightCommand(CopyrightCommand):
    """Inserts the copyright text at the top of the file."""

    def description(self, *args):
        """Describes the command."""
        return "Inserts the copyright text at the location of the current selection."

    def on_owner_selected(self):
        """Finishes inserting the copyright text after the owner is selected."""
        year = datetime.date.today().year
        location = self.determine_location()
        text = self.format_text(year, self.selected_owner)
        copyrightText = self.__build_comment(text)

        self.view.insert(self.edit, location, copyrightText)

    def run(self, edit):
        """Inserts the appropriate copyright text at the top of the file."""
        try:
            self.edit = edit
            self.__get_owner()

        except MissingOwnerException:
            self.handle_missing_owner_exception()

    def determine_location(self):
        """Figures out the right location for the copyright text."""
        region = self.view.full_line(0)
        line = self.view.substr(region)
        if re.match("^#!", line):
            return region.end()
        else:
            return 0

    def get_comment_settings(self):
        """Determines the appropriate comment characters for the currently selected syntax."""
        lineComments, blockComments = comment.build_comment_data(self.view, 0)
        lang = self.get_language_descriptor()
        overrideLanguages = self.settings.get(constants.SETTING_LANGUAGES_USE_LINE_COMMENTS)

        if len(lineComments) == 0 and len(blockComments) == 0:
            self.commentType = constants.COMMENT_TYPE_LINE
            self.firstLine = u"# "
            self.middleLine = u"# "
            self.lastLine = u"# "
        elif lang in overrideLanguages or (len(blockComments) == 0 and len(lineComments) > 0):
            self.commentType = constants.COMMENT_TYPE_LINE
            self.firstLine = lineComments[0][0]
            self.middleLine = lineComments[0][0]
            self.lastLine = lineComments[0][0]
        else:
            self.commentType = constants.COMMENT_TYPE_BLOCK
            self.firstLine = blockComments[0][0]
            self.middleLine = u""
            self.lastLine = blockComments[0][1]

    def get_language_descriptor(self):
        """Gets the language for the current view."""
        longLanguage = self.view.settings().get(u'syntax')
        match = re.search("/([^/]+)\\.tmLanguage$", longLanguage)
        if match:
            return match.group(1)

        return None

    def __build_comment(self, text):
        """Builds a comment and puts the given text into it."""
        self.get_comment_settings()
        if self.commentType == constants.COMMENT_TYPE_LINE:
            return self.__build_line_comment(text)
        else:
            return self.__build_block_comment(text)

    def __build_block_comment(self, text):
        """Builds a block comment using the given text."""
        endings = u'\n'
        padding = self.__get_padding()
        copyright = u""

        def make_comment(line):
            return self.middleLine + line + endings

        def concatenate(x, y):
            return x + y

        if padding == 0:
            return self.firstLine + u" " + text + u" " + self.lastLine + endings

        copyright += self.firstLine.strip() + endings

        for i in range(padding - 1):
            copyright += self.middleLine.strip() + endings

        lines = map(make_comment, text.split(endings))
        copyright += reduce(concatenate, lines)

        for i in range(padding - 1):
            copyright += self.middleLine.strip() + endings

        copyright += self.lastLine.strip() + endings

        return copyright

    def __build_line_comment(self, text):
        """Builds a line comment block using the given text."""
        endings = u'\n'
        padding = self.__get_padding()
        copyright = u""

        def make_comment(line):
            return self.middleLine + line + endings

        def concatenate(x, y):
            return x + y

        for i in range(padding):
            copyright += self.firstLine.strip() + endings

        lines = map(make_comment, text.split(endings))
        copyright += reduce(concatenate, lines)

        for i in range(padding):
            copyright += self.lastLine.strip() + endings

        return copyright

    def __get_owner(self):
        """Gets the copyright owner name that should be used in the copyright message."""
        owners = self.settings.get(constants.SETTING_OWNERS)

        if not owners or len(owners) == 0:
            raise MissingOwnerException()

        if type(owners).__name__ == "unicode":
            self.selected_owner = owners
            self.on_owner_selected()

        def on_quick_panel_done(index):
            self.selected_owner = owners[index]
            self.on_owner_selected()

        sublime.active_window().show_quick_panel(owners, on_quick_panel_done)

    def __get_padding(self):
        """Gets the padding setting or the default if not set."""
        padding = self.settings.get(constants.SETTING_PADDING)
        if padding is None:
            padding = 1

        return padding
