#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

import constants
import datetime
import re

from CopyrightCommand import CopyrightCommand
from Exception import MissingOwnerException


class UpdateCopyrightCommand(CopyrightCommand):
    """Updates the copyright text, if present."""

    def __init__(self, view):
        """Initializes the update copyright command."""
        CopyrightCommand.__init__(self, view)
        self.patterns = None
        self.matched_pattern = None
        self.edit = None

    def run(self, edit):
        """Searches for the copyright text and replaces it, if necessary."""
        try:
            self.edit = edit
            self.__update_copyright()

        except MissingOwnerException:
            self.handle_missing_owner_exception()

    def __find_copyright(self):
        """Finds the first matching copyright text."""
        patterns = self.get_patterns()

        for pattern in patterns:
            region = self.view.find(pattern, 0)
            if region is not None and self.__is_in_comment(region):
                self.matched_pattern = pattern
                return region

        return None

    def __get_old_year(self, region, pattern):
        """Extract the old year from the pre-existing copyright text."""
        text = self.view.substr(region)
        match = re.match(pattern, text)
        return match.group(1)

    def get_owners(self):
        """Gets the list of owners from the settings."""
        owners = self.settings.get(constants.SETTING_OWNERS)

        if not owners or len(owners) == 0:
            raise MissingOwnerException()

        if type(owners).__name__ == "unicode":
            return [owners]

        return owners

    def get_patterns(self):
        """Gets the patterns to use to find the copyright text."""
        owners = self.get_owners()

        if self.patterns is None:
            self.patterns = {}
            for owner in owners:
                self.patterns[self.format_pattern("(\d+)(-\d+)?", owner)] = owner

        return self.patterns

    def __is_in_comment(self, region):
        """Determines if the entire region is encapsulated by a comment."""
        point = region.begin()
        if self.view.scope_name(point).find('comment') != -1:
            comment_region = self.view.extract_scope(point)
            if comment_region.begin() <= region.begin() and comment_region.end() >= region.end():
                return True

        return False

    def __replace_copyright(self, region):
        """Replaces the copyright text by updating the year to span from the original year to the current one."""
        if region is not None:
            pattern = self.matched_pattern
            oldYear = self.__get_old_year(region, pattern)
            newYear = str(datetime.date.today().year)
            if oldYear != newYear:
                self.__replace_match(region, oldYear, newYear)

        self.matched_pattern = None

    def __replace_match(self, region, oldYear, newYear):
        """Replace the old copyright text with the new copyright text."""
        owner = self.patterns[self.matched_pattern]
        message = self.format_text(oldYear + "-" + newYear, owner)
        self.view.replace(self.edit, region, message)
        self.edit = None

    def __update_copyright(self):
        """Finds the copyright text and replaces it."""
        region = self.__find_copyright()
        self.__replace_copyright(region)
