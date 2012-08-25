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
    pattern = self.__format_pattern()
    region = self.__find_pattern(pattern)

    if region:
      oldYear = self.__get_old_year(region, pattern)
      newYear = str(datetime.date.today().year)
      if oldYear != newYear:
        self.__replace_match(edit, region, oldYear, newYear)

  def __format_pattern(self):
    '''
    Takes the copyright message and turns it into a pattern to find pre-existing copyright text.
    '''
    message = self.settings.get(constants.SETTING_COPYRIGHT_MESSAGE)
    message = message.replace("%o", "ooowner")
    message = message.replace("%y", "yyyear")
    message = re.escape(message)
    message = message.replace("ooowner", self.get_owner())
    pattern = message.replace("yyyear", "(\d+)(-\d+)?")

    return pattern

  def __find_pattern(self, pattern):
    '''
    Find the pattern in the view and return the Region, if it exists.
    '''
    return self.view.find(pattern, 0)

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
