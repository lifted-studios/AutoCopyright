# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

import os
import sys

# Required so that the comment module can be imported reliably on startup
package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
default_package_dir = os.path.join(package_dir, 'Default')
sys.path.append(default_package_dir)

import comment
import constants
import datetime
import re

from CopyrightCommand import CopyrightCommand
from Exception import MissingOwnerException

class InsertCopyrightCommand(CopyrightCommand):
  '''
  Inserts the copyright text at the top of the file.
  '''
  def description(self, *args):
    '''
    Describes the command.
    '''
    return "Inserts the copyright text at the location of the current selection."

  def run(self, edit):
    '''
    Executes the copyright command by inserting the appropriate copyright text at the current selection point.
    '''
    try:
      self.__insert_copyright(edit)

    except MissingOwnerException:
      self.__handle_missing_owner_exception()

  def __build_block_comment(self, text):
    '''
    Builds a block comment and puts the given text into it.
    '''
    self.__get_block_comment_settings()
    endings = self.__get_line_endings()

    def make_comment(line): return self.middleLine + line + endings
    def concatenate(x, y): return x + y

    comment = self.firstLine + endings
    lines = map(make_comment, text.split(endings))
    comment += reduce(concatenate, lines)
    comment += self.lastLine + endings
    return comment

  def __determine_location(self):
    '''
    Figures out the right location for the copyright text.
    '''
    region = self.view.full_line(0)
    line = self.view.substr(region)
    if re.match("^#!", line):
      return region.end()
    else:
      return 0

  def __get_block_comment_settings(self):
    '''
    Determines the appropriate block comment characters for the currently selected syntax.
    '''
    lineComments, blockComments = comment.build_comment_data(self.view, 0)
    if len(blockComments) == 0:
      self.firstLine = lineComments[0][0]
      self.middleLine = lineComments[0][0]
      self.lastLine = lineComments[0][0]
    else:
      self.firstLine = blockComments[0][0]
      self.middleLine = ''
      self.lastLine = blockComments[0][1]

  def __get_line_endings(self):
    '''
    Gets the appropriate line endings for the view.

    Unix and Mac OS X use the LF character.  Windows uses the CRLF pair.  Old versions of Mac OS used just the CR character.
    '''
    if self.view.line_endings() == constants.LINE_ENDING_UNIX:
      return u'\u000a'
    elif self.view.line_endings() == constants.LINE_ENDING_WINDOWS:
      return u'\u000a\u000d'
    else:
      return u'\u000d'

  def __insert_copyright(self, edit):
    '''
    Inserts the copyright message into the view.
    '''
    year = datetime.date.today().year
    owner = self.get_owner()
    location = self.__determine_location()
    text = self.format_text(year, owner)
    copyrightText = self.__build_block_comment(text)

    self.view.insert(edit, location, copyrightText)
