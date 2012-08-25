# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

import sublime
import sublime_plugin

class AutoCopyrightEventListener(sublime_plugin.EventListener):
  '''
  Listener for application events.
  '''
  def on_pre_save(self, view):
    '''
    Called just before the view is saved.
    '''
    view.run_command('update_copyright')
