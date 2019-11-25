from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_crawler():
    process = CrawlerProcess(get_project_settings())
    process.crawl('events')
    process.start()  # the script will block here until the crawling is finished
def run_crawler(request):
    """
    Takes a HTTP Cloud Function request and starts the `event` spider.
    :param request:
    """
