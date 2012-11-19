#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

import os
import tempfile

from MockEdit import MockEdit
from MockRegion import MockRegion
from MockSettings import MockSettings
from MockView import MockView
from MockWindow import MockWindow

settings = MockSettings()
window = MockWindow()


def active_window():
    """Returns a mock window."""
    return window


def error_message(message):
    """Does nothing."""
    pass


def load_settings(file):
    """Simply returns the default mock settings."""
    return settings


def packages_path():
    """Returns a fake packages path."""
    return os.path.join(tempfile.gettempdir(), "sublime_tests")
