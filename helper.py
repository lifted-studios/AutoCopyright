#
# Copyright (c) 2012-2013 by Lifted Studios.  All Rights Reserved.
#

import AutoCopyright.constants
import sublime


def error_message(message):
    """Displays an error message dialog to the user."""
    text = AutoCopyright.constants.PLUGIN_NAME + ': ' + message
    sublime.error_message(text)
