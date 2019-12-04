from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet.task import deferLater

process = CrawlerProcess(get_project_settings())


def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(reactor, seconds, lambda: None)


def crash(failure):
    print('oops, spider crashed')
    print(failure.getTraceback())


def _crawl(result, spider):
    deferred = process.crawl(spider)
    deferred.addCallback(lambda results: print('waiting 100 seconds before restart...'))
    deferred.addErrback(crash)  # <-- add errback here
    deferred.addCallback(sleep, seconds=100)
    deferred.addCallback(_crawl, spider)
    return deferred


def run_crawler(request):
    _crawl(None, 'events')
    process.start()
