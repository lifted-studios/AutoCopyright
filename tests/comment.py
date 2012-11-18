#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

line_comment_data = []
block_comment_data = []


def build_comment_data(view, n):
    return line_comment_data, block_comment_data


def set_comment_data(line_comments, block_comments):
    global line_comment_data
    global block_comment_data
    line_comment_data = line_comments
    block_comment_data = block_comments
