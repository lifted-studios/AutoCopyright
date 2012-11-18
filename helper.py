#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

import constants
import sublime


def error_message(message):
    """Displays an error message dialog to the user."""
    text = constants.PLUGIN_NAME + ': ' + message
    sublime.error_message(text)
