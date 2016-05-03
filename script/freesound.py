#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib


def TagsDict(tags_path):
    tags_dict = {}
    with open(tags_path, 'r') as tags_file:
        for line in tags_file:
            line = line.strip()
            if line == '':
                continue
            if line not in tags_dict:
                tags_dict[line] = line
    return tags_dict

def TagsFilter(txt_path, tags_dict):
    tags = []
    with open(txt_path, 'r') as txt_file:
        for line in txt_file:
            line = line.strip()
            items = line.split('=')
            if items[0] == 'tags':
                tags = items[1].split(',')
                break
    for tag in tags:
        if tag in tags_dict:
            print '%s\t%s' % (tag, txt_path)

def TagFilter(txt_path, tag_str):
    tags = []
    with open(txt_path, 'r') as txt_file:
        for line in txt_file:
            line = line.strip()
            items = line.split('=')
            if items[0] == 'tags':
                tags = items[1].split(',')
                break
    for tag in tags:
        if tag == tag_str:
            print txt_path

def DownloadOgg(txt_path):
    # ogg url address
    ogg_url = ''
    with open(txt_path, 'r') as txt_file:
        for line in txt_file:
            line = line.strip()
            items = line.split('=')
            if items[0] == 'ogg':
                ogg_url = items[1]
                break
    # ogg file path
    ogg_path = txt_path[:txt_path.rfind('.')] + '.ogg'
    # download
    ogg_byte = urllib.urlopen(ogg_url).read()
    with open(ogg_path, 'wb') as ogg_file:
        ogg_file.write(ogg_byte)
    print ogg_path

if __name__ == '__main__':
    if not (len(sys.argv) == 3 or len(sys.argv) == 2):
        print 'python %s freesound.list str_tag' % sys.argv[0]
        print 'python %s download.list' % sys.argv[0]
        sys.exit(1)

    if len(sys.argv) == 3:
        #tags_dict = TagsDict(sys.argv[2])
        with open(sys.argv[1], 'r') as list_file:
            for line in list_file:
                path = line.strip()
                if not os.path.exists(path):
                    print 'Warning : cannot find %s' % path
                    continue
                #TagsFilter(path, tags_dict)
                TagFilter(path, sys.argv[2])

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as list_file:
            for line in list_file:
                path = line.strip()
                if not os.path.exists(path):
                    print 'Warning : cannot find %s' % path
                    continue
                DownloadOgg(path)

