import logging
import json

from scrapy.exceptions import NotConfigured
from scrapy import signals, Spider
from youngklm_scraper.youngklm.scrapinghubclient import ScrapingHubClient
from youngklm_scraper.youngklm.slackwebhook import send_message_to_slack_channel

logger = logging.getLogger(__name__)


class EventPublisher(object):

    def __init__(self, scrapinghub_client: ScrapingHubClient, slack_webhook_url: str):
        self.scrapinghub_client = scrapinghub_client
        self.slack_webhook_url = slack_webhook_url
        self.events = []

    @classmethod
    def from_crawler(cls, crawler):
        # Check if our extension is enabled in `settings.py`
        if not crawler.settings.getbool('EVENT_PUBLISHER_ENABLED'):
            raise NotConfigured("EVENT_PUBLISHER_ENABLED setting is False")

        scrapinghub_api_key = crawler.settings.get('SCRAPINGHUB_API_KEY')
        if not scrapinghub_api_key:
            raise NotConfigured("SCRAPINGHUB_API_KEY not configured.")

        scrapinghub_project_id = crawler.settings.getint('SCRAPINGHUB_PROJECT_ID')
        if not scrapinghub_project_id:
            raise NotConfigured("SCRAPINGHUB_PROJECT_ID not configured.")

        slack_webhook_url = crawler.settings.get('SLACK_WEBHOOK_URL')
        if not slack_webhook_url:
            raise NotConfigured("SLACK_WEBHOOK_URL not configured.")

        client = ScrapingHubClient(api_key=scrapinghub_api_key, project_id=scrapinghub_project_id)
        extension = cls(scrapinghub_client=client, slack_webhook_url=slack_webhook_url)

        # connect the extension object to signals
        crawler.signals.connect(extension.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(extension.item_scraped, signal=signals.item_scraped)

        return extension

    def item_scraped(self, item, spider, response):
        self.events.append(item)

    def spider_closed(self, spider: Spider, reason: str):
        if reason is not "finished":
            return

        previous_events = self.scrapinghub_client.get_stored_items(ScrapingHubClient.EVENTS_KEY)
        latest_events = self.events

        def events_updated():
            previous_urls = [event['event_url'] for event in previous_events]
            latest_urls = [event['event_url'] for event in latest_events]
            return set(previous_urls) != set(latest_urls)

        if events_updated():
            def post_new_events():
                logging.info('Posting on Slack.')

                urls = [event['event_url'] for event in latest_events]
                send_message_to_slack_channel(web_hook_url=self.slack_webhook_url,
                                              payload="New events on Youngklm.nl/events")
                send_message_to_slack_channel(web_hook_url=self.slack_webhook_url, payload=urls)

                logging.info('Crawled new events!')
                self.scrapinghub_client.store_item_in_collections(ScrapingHubClient.EVENTS_KEY, latest_events)

                if self.slack_webhook_url:
                    post_new_events()
                    pass

        else:
            logging.info('Recent items not newer than previous.')
