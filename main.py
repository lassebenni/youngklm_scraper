from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor


def run_crawler(request):
    """
    Takes a HTTP Cloud Function request and starts the `event` spider.
    :param request:
    """
    runner = CrawlerRunner(get_project_settings())

    d = runner.crawl('events')
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
