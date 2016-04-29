# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FreesoundItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index = scrapy.Field()
    title = scrapy.Field()
    filetype = scrapy.Field()
    duration = scrapy.Field()
    size = scrapy.Field()
    rate = scrapy.Field()
    bit = scrapy.Field()
    channel = scrapy.Field()
    tags = scrapy.Field()
    # separator row
    count = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    desc = scrapy.Field()
    waveform = scrapy.Field()
    spectrum = scrapy.Field()
    mp3 = scrapy.Field()
    ogg = scrapy.Field()
    wav = scrapy.Field()
    url = scrapy.Field()


