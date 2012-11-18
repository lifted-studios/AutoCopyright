#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#


class MockView:
    """Mock View class for testing."""
    def __init__(self):
        self.insertCalled = False

    def full_line(self, pos):
        return [0, 0]

    def insert(self, edit, location, text):
        self.edit = edit
        self.location = location
        self.text = text
        self.insertCalled = True

    def line_endings(self):
        return 'Unix'

    def substr(self, region):
        return ""
