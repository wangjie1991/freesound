# -*- coding: utf-8 -*-

import os
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from pybloomfilter import BloomFilter
from freesound.items import FreesoundItem

class LinkFilter():
    def __init__(self):
        if os.path.exists('bloomfilter'):
            self.bloomfilter = BloomFilter.open('bloomfilter')
        else:
            self.bloomfilter = BloomFilter(1000000, 0.01, 'bloomfilter')

    def process(self, links):
        new_links = []
        for link in links:
            if not self.bloomfilter.add(link.url):
                new_links.append(link)
        return new_links


class FreesoundSpider(CrawlSpider):
    name = 'freesound'
    allowed_domains = ['www.freesound.org']
    start_urls = ['http://www.freesound.org/people/']

    allow_url = [
                    # r'http://www.freesound.org/browse/tags/.*',
                    r'http://www.freesound.org/people/\w*$',
                    r'http://www.freesound.org/people/\w+/sounds/.*',
                    r'http://www.freesound.org/people/\w+/packs/.*',
                    r'http://www.freesound.org/people/\w+/downloaded_packs/.*',
                    r'http://www.freesound.org/people/\w+/downloaded_sounds/.*',
                    r'http://www.freesound.org/people/\w+/followers/$',
                ]
    deny_url =  [
                    r'http://www.freesound.org/people/\w+/sounds/\d+/flag/$',
                    r'http://www.freesound.org/people/\w+/sounds/\d+/geotag/$',
                    r'http://www.freesound.org/people/\w+/sounds/\d+/downloaders/.*',
                    r'http://www.freesound.org/people/\w+/packs/\d+/downloaders/.*',
                ]
    parse_url =  [ r'http://www.freesound.org/people/\w+/sounds/\d+/$' ]

    lf = LinkFilter()

    rules = [
                Rule(LinkExtractor(allow=parse_url, deny=deny_url), callback='parse_item',
                     follow=True, process_links=lf.process),
                Rule(LinkExtractor(allow=allow_url, deny=deny_url+parse_url),
                     process_links=lf.process)
            ]

    def parse_item(self, response):
        item = FreesoundItem()

        info = response.url.rstrip('/')
        item['index'] = info[info.rfind('/')+1:]

        info = response.xpath('//head/title/text()').extract()[0]
        item['title'] = info[info.find('"')+1:info.rfind('"')]

        info = response.xpath('//dl[@id="sound_information_box"]/dd/text()').extract()
        if len(info) == 6:
            item['filetype'] = info[0]
            item['duration'] = info[1]
            item['size'] = info[2]
            item['rate'] = info[3]
            item['bit'] = info[4]
            item['channel'] = info[5]
        elif len(info) == 5:
            item['filetype'] = info[0]
            item['duration'] = info[1]
            item['size'] = info[2]
            item['rate'] = ''
            item['bit'] = ''
            item['channel'] = info[4]
        else:
            item['filetype'] = ''
            item['duration'] = ''
            item['size'] = ''
            item['rate'] = ''
            item['bit'] = ''
            item['channel'] = ''

        # item tags
        tags = ''
        info = response.xpath('//ul[@class="tags"]/li//text()').extract()
        for tag in info:
            tags += ',' + tag
        tags = tags.strip(',')
        item['tags'] = tags

        item['count'] = response.xpath('//div[@id="download_text"]//b/text()').extract()[0]
        item['author'] = response.xpath('//div[@id="sound_author"]//text()').extract()[0]
        item['date'] = response.xpath('//div[@id="sound_date"]//text()').extract()[0]

        # item desc
        desc = ''
        info = response.xpath('//div[@id="sound_description"]/p/text()').extract()
        for line in info:
            desc += ' ' + line
        desc = desc.strip()
        item['desc'] = desc

        div = response.xpath('//div[@id="single_sample_player"]')

        # waveform
        info = div.xpath('.//a[@class="waveform"]/@href').extract()[0]
        if info[0] == '/':
            info = 'http://www.freesound.org' + info
        item['waveform'] = info

        # spectrum
        info = div.xpath('.//a[@class="spectrum"]/@href').extract()[0]
        if info[0] == '/':
            info = 'http://www.freesound.org' + info
        item['spectrum'] = info

        # mp3
        info = div.xpath('.//a[@class="mp3_file"]/@href').extract()[0]
        if info[0] == '/':
            info = 'http://www.freesound.org' + info
        item['mp3'] = info

        # ogg
        info = div.xpath('.//a[@class="ogg_file"]/@href').extract()[0]
        if info[0] == '/':
            info = 'http://www.freesound.org' + info
        item['ogg'] = info

        # wav
        info = response.xpath('//div[@id="download"]/a/@href').extract()[0]
        if info[0] == '/':
            info = 'http://www.freesound.org' + info
        item['wav'] = info

        # url
        item['url'] = response.url

        return item


