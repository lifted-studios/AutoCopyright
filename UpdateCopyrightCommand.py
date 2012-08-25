# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

import constants
import datetime
import re

from CopyrightCommand import CopyrightCommand
from Exception import MissingOwnerException

class UpdateCopyrightCommand(CopyrightCommand):
  '''
  Updates the copyright text, if present.
  '''
  def run(self, edit):
    '''
    Executes the update command by searching for the copyright text and replacing it, if necessary.
    '''
    try:
      self.__update_copyright(edit)

    except MissingOwnerException:
      self.handle_missing_owner_exception()

  def __update_copyright(self, edit):
    '''
    Finds the copyright text and replaces it by updating the year if it has changed.
    '''
    pattern = self.format_pattern("(\d+)(-\d+)?", self.get_owner())
    region = self.view.find(pattern, 0)

    if region:
      oldYear = self.__get_old_year(region, pattern)
      newYear = str(datetime.date.today().year)
      if oldYear != newYear:
        self.__replace_match(edit, region, oldYear, newYear)

  def __get_old_year(self, region, pattern):
    '''
    Extract the old year from the pre-existing copyright text.
    '''
    text = self.view.substr(region)
    match = re.match(pattern, text)
    return match.group(1)

  def __replace_match(self, edit, region, oldYear, newYear):
    '''
    Replace the old copyright text with the new copyright text.
    '''
    owner = self.get_owner()
    message = self.format_text(oldYear + "-" + newYear, owner)
    self.view.replace(edit, region, message)
