from datetime import datetime

import scrapy


class EventsSpider(scrapy.Spider):
    name = 'events'
    allowed_domains = ['youngklm.nl']
    start_urls = ['http://youngklm.nl/events']

    def parse(self, response):
        events = response.xpath('//*[@class="col-md-12"]')

        for event in events:
            url = event.xpath('.//*[@class="block_link"]/@href').extract_first()
            date = event.xpath('.//*[@class="meta"]/text()').extract_first()
            text = event.xpath('.//h2/text()').extract_first()

            # format "day-month-year hour:minute"
            datetime_format = f'%d-%m-%y %H:%M'
            now = datetime.strftime(datetime.now(), format=datetime_format)

            yield {
                'crawl_datetime': now,
                'event_date': date,
                'event_text': text,
                'event_url': url
            }
