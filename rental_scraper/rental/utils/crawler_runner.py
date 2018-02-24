# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.crawler import CrawlerRunner


class RentalCrawlerRunner(CrawlerRunner):
    """
    Crawler runner.

    Collects items and returns output after finishing crawl.
    """

    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        """Execute the web crawler.

        :param crawler_or_spidercls: Crawler of spider class
        :type crawler_or_spidercls: RentalCrawler
        :param *args: list of args
        :type *args: List
        :param **kwargs: dict of args
        :type **kwargs: Dict
        :return: defered results
        :rtype: defered
        """
        print("executing crawler runner")

        # keep all items scraped
        self.items = []

        # create crawler (Same as in base CrawlerProcess)
        crawler = self.create_crawler(crawler_or_spidercls)

        # handle each item scraped
        crawler.signals.connect(self.item_scraped, signals.item_scraped)

        # create Twisted.Deferred launching crawl
        dfd = self._crawl(crawler, *args, **kwargs)

        # add callback - when crawl is done cal return_items
        dfd.addCallback(self.return_items)
        print("finishing crawler runner")
        return dfd

    def item_scraped(self, item, response, spider):
        """Store the item scraped into the item list.

        :param item: Scraped item
        :type item: RentalItem
        :param response: Scrapy response
        :type response: Response
        :param spider: Web Scraper instance
        :type spider: RentalCrawler
        """
        self.items.append(item)

    def return_items(self, result):
        """Return the list of items scraped.

        :param result: [description]
        :type result: [type]
        :return: List of scraped items
        :rtype: List
        """
        return self.items
