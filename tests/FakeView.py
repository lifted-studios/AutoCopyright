#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

import re

from MockRegion import MockRegion


class FakeView:
    """Fake View class for testing."""
    def __init__(self, contents=None):
        self.contents = contents

    def find(self, pattern, pos):
        text = self.contents[pos:-1]
        match = re.search(pattern, text)
        if match:
            return MockRegion(match.start + pos, match.end + pos)

        return None
