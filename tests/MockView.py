#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

import re

from MockRegion import MockRegion


class MockView:
    """Mock View class for testing."""
    def __init__(self, contents=None):
        self.insertCalled = False
        self.full_line_region = None
        self.substr_string = None
        self.contents = contents

    def find(self, pattern, pos):
        text = self.contents[pos:-1]
        match = re.search(pattern, text)
        if match:
            return MockRegion(match.start + pos, match.end + pos)

        return None

    def full_line(self, pos):
        return self.full_line_region or (0, 0)

    def insert(self, edit, location, text):
        self.edit = edit
        self.location = location
        self.text = text
        self.insertCalled = True

    def substr(self, region):
        return self.substr_string or u""
