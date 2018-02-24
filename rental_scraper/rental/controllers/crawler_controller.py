# -*- coding: utf-8 -*-

"""Module docstring."""
import json

import mongoengine
from twisted.internet import defer

from models.crawler_config import CrawlerConfig
from settings import DATA_BASE
from spiders.rental_crawler import RentalCrawler
from utils.crawler_runner import RentalCrawlerRunner


@defer.inlineCallbacks
def execute_chaining_crawler():
    """Execute chaining crawler.

    :return: Crawler results
    :rtype: defer
    """
    result = ""
    runner = RentalCrawlerRunner()
    mongoengine.connect(**DATA_BASE)
    for rental in CrawlerConfig.objects:
        print("initiating {0}".format(rental.name))
        crawler_result = yield runner.crawl(
            RentalCrawler, crawler_config=rental)
        result += yield return_spider_output(crawler_result)
    defer.returnValue(result)


def return_spider_output(output):
    """Turn items into dictionaries.

    :param output: items scraped by CrawlerRunner
    :type output: List
    :return: json with list of items
    :rtype: json
    """
    # TODO Maybe use Scrapy JSON serializer here
    return json.dumps([dict(item) for item in output])
