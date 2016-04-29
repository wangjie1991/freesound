# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os


class FreesoundPipeline(object):
    def process_item(self, item, spider):
        text = ''

        if item['index'] == '':
            return item

        line = 'index=%s\n' % item['index']
        text += line
        line = 'title=%s\n' % item['title']
        text += line
        line = 'filetype=%s\n' % item['filetype']
        text += line
        line = 'duration=%s\n' % item['duration']
        text += line
        line = 'size=%s\n' % item['size']
        text += line
        line = 'rate=%s\n' % item['rate']
        text += line
        line = 'bit=%s\n' % item['bit']
        text += line
        line = 'channel=%s\n' % item['channel']
        text += line
        line = 'tags=%s\n' % item['tags']
        text += line
        line = 'count=%s\n' % item['count']
        text += line
        line = 'author=%s\n' % item['author']
        text += line
        line = 'date=%s\n' % item['date']
        text += line
        line = 'desc=%s\n' % item['desc']
        text += line
        line = 'waveform=%s\n' % item['waveform']
        text += line
        line = 'spectrum=%s\n' % item['spectrum']
        text += line
        line = 'mp3=%s\n' % item['mp3']
        text += line
        line = 'ogg=%s\n' % item['ogg']
        text += line
        line = 'wav=%s\n' % item['wav']
        text += line
        line = 'url=%s\n' % item['url']
        text += line

        fdir = '/Users/wangjie/Downloads/freesound'
        if not os.path.exists(fdir):
            os.makedirs(fdir)

        name = '%s/%s.txt' % (fdir, item['index'])
        with open(name, 'w') as fout:
            fout.write(text.encode('utf-8'))
        return item


