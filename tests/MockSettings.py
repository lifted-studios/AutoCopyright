#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#


class MockSettings:
    """Mock settings for Sublime Text."""
    def __init__(self):
        self.settings = {}

    def get(self, name):
        """Gets the named setting."""
        return self.settings[name]

    def set(self, name, value):
        """Sets the named setting."""
        self.settings[name] = value
