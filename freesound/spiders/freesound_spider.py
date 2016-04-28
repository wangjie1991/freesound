# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from pybloomfilter import BloomFilter
from freesound.items import FreesoundItem


class FreesoundSpider(CrawlSpider):
    name = 'freesound'
    allowed_domains = ['www.freesound.org']
    start_urls = ['http://www.freesound.org/people/']

    parse_url = [r'http://www.freesound.org/people/\w+/sounds/\d+/']
    follow_url = [r'http://www.freesound.org/people/.*', 
                  r'http://www.freesound.org/browse/tags/.*']

    #bloomfilter = BloomFilter(100000, 0.01, 'freesound.bf')
    #bloomfilter = BloomFilter.open('freesound.bf')

    rules = [
                Rule(LinkExtractor(allow=parse_url), callback='parse_item',
                     follow=True, process_links=link_filter),
                Rule(LinkExtractor(allow=follow_url, deny=parse_url), 
                     process_links=link_filter)
            ]

    def link_filter(self, links):
        '''
        new_links = []
        for link in links:
            if not self.bloomfilter.add(link.url):
                new_links.append(link)
        return new_links
        '''
        return links

    def parse_item(self, response):
        item = FreesoundItem()

        info = response.url.rstrip('/')
        item['index'] = info[info.rfind('/')+1:]

        info = response.xpath('//head/title/text()').extract()[0]
        item['title'] = info[info.find('"')+1:info.rfind('"')]

        info = response.xpath('//dl[@id="sound_information_box"]/dd/text()').extract()
        item['filetype'] = info[0]
        item['duration'] = info[1]
        item['size'] = info[2]
        item['rate'] = info[3]
        item['bit'] = info[4]
        item['channel'] = info[5]

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

        return item


