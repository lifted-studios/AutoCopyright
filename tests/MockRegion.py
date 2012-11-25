#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#


class MockRegion:
    """Region class for testing."""
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def begin(self):
        if self.b > self.a:
            return self.a
        else:
            return self.b

    def end(self):
        if self.b > self.a:
            return self.b
        else:
            return self.a
