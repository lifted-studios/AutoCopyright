#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.dirname(test_dir)
sys.path.append(test_dir)
sys.path.append(source_dir)

import unittest


class TestUpdateCopyrightCommand(unittest.TestCase):
    pass
