# -*- coding: utf-8 -*-

"""Module docstring."""
import json

import mongoengine
from twisted.internet import defer

from models.crawler_config import CrawlerConfig
from settings import DATA_BASE
from utils.crawler_runner import RentalCrawlerRunner
from controllers.crawler_register import CRAWLER_REGISTER


@defer.inlineCallbacks
def execute_chaining_crawler(filters):
    """Execute chaining crawler.

    :return: Crawler results
    :rtype: defer
    """
    result = ""
    runner = RentalCrawlerRunner()
    mongoengine.connect(**DATA_BASE)
    for rental in CrawlerConfig.objects(status="ACTIVE"):
        print("Initiating {0}".format(rental.name))
        rental_crawler = CRAWLER_REGISTER[rental.name]
        crawler_result = yield runner.crawl(
            rental_crawler, crawler_config=rental, filters=filters)
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
