#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
书签模块
"""

import os
import json

__all__ = ['add_bookmark', 'list_bookmarks',
    'delete_bookmark']

BM_DB_PATH = os.path.expanduser('~/.bookmark')


class Bookmark(object):

    """书签类"""

    def __init__(self, text, tags=None):
        """TODO: to be defined.

        :text: 书签内容
        :tags: 标签

        """
        self.text = text
        if not tags:
            tags = []
        self.tags = tags

    def to_dict(self):
        return json.loads(self.to_json())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


def add_bookmark(text, tags=None):
    _add_bookmark(text, tags)

def _add_bookmark(text, tags=None):
    """添加书签"""
    bm = Bookmark(text, tags)
    with open(BM_DB_PATH, 'a') as f:
        f.write(bm.to_json())
        f.write('\n')

def list_bookmarks(tags=None):
    return _list_bookmark(tags)

def _list_bookmark(tags=None):
    """添加书签"""
    if not tags:
        tags = []
    with open(BM_DB_PATH, 'r') as f:
        lines = f.readlines()

    bookmarks = []
    for line in lines:
        if not line or line == '\n':
            continue
        bm = Bookmark(**json.loads(line))

        command_tags = [ o for o in tags if o in bm.tags ]
        add_flag1 = not tags
        add_flag2 = tags and command_tags
        is_add = add_flag1 or add_flag2

        if is_add:
            bookmarks.append(bm)
    return bookmarks


def delete_bookmark(text):
    _delete_bookmark(text)

def _delete_bookmark(text):
    """删除书签"""
    with open(BM_DB_PATH, 'r') as f:
        lines = f.readlines()
    new_lines = []
    count = 0
    for line in lines:
        if not line or line == '\n':
            continue
        bm = Bookmark(**json.loads(line))
        if bm.text == text:
            count += 1
            continue
        if line:
            new_lines.append(line)
    with open(BM_DB_PATH, 'w') as f:
        f.write('\n'.join(new_lines))
    return count

