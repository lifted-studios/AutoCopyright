#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#


class MockView:
    """Mock View class for testing."""
    def __init__(self):
        self.insertCalled = False
        self.full_line_region = None
        self.substr_string = None
        self.endings = u'Unix'

    def full_line(self, pos):
        return self.full_line_region or (0, 0)

    def insert(self, edit, location, text):
        self.edit = edit
        self.location = location
        self.text = text
        self.insertCalled = True

    def line_endings(self):
        return u'Unix'

    def set_line_endings(self, endings):
        self.endings = endings

    def substr(self, region):
        return self.substr_string or u""
