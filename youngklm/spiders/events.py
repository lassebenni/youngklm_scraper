# -*- coding: utf-8 -*-
import scrapy
import scrapy-slackbot

class EventsSpider(scrapy.Spider):
    name = 'events'
    allowed_domains = ['youngklm.nl']
    start_urls = ['http://youngklm.nl/events']

    def parse(self, response):
        test_setting = self.settings['TEST_SETTING']
        print(test_setting)

        events = response.xpath('//*[@class="col-md-12"]')

        for event in events:
            url = event.xpath('.//*[@class="block_link"]/@href').extract_first()
            date = event.xpath('.//*[@class="meta"]/text()').extract_first()
            text = event.xpath('.//h2/text()').extract_first()

            yield {
                'date': date,
                'text': text,
                'url': url
            }
