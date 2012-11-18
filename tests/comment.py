#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

block_comments = ([(u'// ', False), (u'//', False)], [(u'/*', u'*/', True), (u'/*', u'*/', True)])
line_comments = ([(u'# ', False), (u'#', False)], [])
no_comments = ([], [])

comment_data = ()


def build_comment_data(view, n):
    return comment_data


def set_comment_data(data):
    global comment_data
    comment_data = data


def set_block_comments():
    set_comment_data(block_comments)


def set_line_comments():
    set_comment_data(line_comments)


def set_no_comments():
    set_comment_data(no_comments)
