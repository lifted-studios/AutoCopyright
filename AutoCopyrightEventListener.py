#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

import sublime_plugin


class AutoCopyrightEventListener(sublime_plugin.EventListener):
    """Overrides the on_pre_save hook to allow for updating the copyright in a file automatically."""

    def on_pre_save(self, view):
        """Called just before the view is saved."""
        view.run_command('update_copyright')
