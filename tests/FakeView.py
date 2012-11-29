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
        text = self.contents[pos:]
        match = re.search(pattern, text)
        if match:
            return MockRegion(match.start() + pos, match.end() + pos)

        return None

    def extract_scope(self, point):
        return MockRegion(0, len(self.contents))

    def replace(self, edit, region, text):
        before = self.contents[0:region.begin()]
        after = self.contents[region.end():]
        self.contents = before + text + after

    def scope_name(self, point):
        return u'comment'

    def substr(self, region):
        return self.contents[region.begin():region.end()]
