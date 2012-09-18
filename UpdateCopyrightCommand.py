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

  def __init__(self, view):
    '''
    Initializes the update copyright command.
    '''
    CopyrightCommand.__init__(self, view)
    self.pattern = None
    self.edit = None

  def run(self, edit):
    '''
    Executes the update command by searching for the copyright text and replacing it, if necessary.
    '''
    try:
      self.edit = edit
      self.__update_copyright()

    except MissingOwnerException:
      self.handle_missing_owner_exception()

  def __find_copyright(self):
    '''
    Finds the copyright text.
    '''
    pattern = self.__get_pattern()
    return self.view.find(pattern, 0)

  def __get_old_year(self, region, pattern):
    '''
    Extract the old year from the pre-existing copyright text.
    '''
    text = self.view.substr(region)
    match = re.match(pattern, text)
    return match.group(1)

  def __get_pattern(self):
    '''
    Gets the pattern to use to find the copyright text.
    '''
    if self.pattern is None:
      self.pattern = self.format_pattern("(\d+)(-\d+)?", self.get_owner())

    return self.pattern

  def __replace_copyright(self, region):
    '''
    Replaces the copyright text by updating the year to span from the original year to the current one.
    '''
    if region:
      pattern = self.__get_pattern()
      oldYear = self.__get_old_year(region, pattern)
      newYear = str(datetime.date.today().year)
      if oldYear != newYear:
        self.__replace_match(region, oldYear, newYear)

  def __replace_match(self, region, oldYear, newYear):
    '''
    Replace the old copyright text with the new copyright text.
    '''
    owner = self.get_owner()
    message = self.format_text(oldYear + "-" + newYear, owner)
    self.view.replace(self.edit, region, message)

  def __update_copyright(self):
    '''
    Finds the copyright text and replaces it.
    '''
    region = self.__find_copyright()
    self.__replace_copyright(region)
