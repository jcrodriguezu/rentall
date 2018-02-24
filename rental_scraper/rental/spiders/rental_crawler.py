# -*- coding: utf-8 -*-
"""Rental crawler."""

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from spiders.items import RentalItem
from errors import CrawlerConfigNotProvidedError


class RentalCrawler(CrawlSpider):
    """Generic crawler for house lease."""

    name = "rental_crawler"

    def __init__(self, crawler_config, *args, **kwargs):
        """Rental Crawler constructor."""
        if not crawler_config:
            raise CrawlerConfigNotProvidedError

        self.name = crawler_config.name
        self.domain = crawler_config.domain
        self.allowed_domains = [self.domain]
        self.start_urls = [crawler_config.start_url]
        self.pagination_regex = crawler_config.pagination_regex
        self.xpath_item_list = crawler_config.xpath_item_list
        self.xpath_neighborhood = crawler_config.xpath_neighborhood
        self.xpath_square_meters = crawler_config.xpath_square_meters
        self.xpath_price = crawler_config.xpath_price
        self.xpath_url = crawler_config.xpath_url
        self.xpath_detail = crawler_config.xpath_detail
        self.xpath_title = crawler_config.xpath_title
        self.xpath_code = crawler_config.xpath_code
        self.xpath_next = crawler_config.xpath_next
        if self.pagination_regex:
            self.rules = [
                Rule(
                    LinkExtractor(
                        allow=r'{0}'.format(self.pagination_regex),
                        restrict_xpaths=self.xpath_next
                    ),
                    callback="parse_item",
                    follow=False  # Change this to follow the next page
                )
            ]
        super(RentalCrawler, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        """Parse the items according to the crawler config data.

        :param response: request response
        :type response: Response
        :return: Crawler item
        :rtype: RentalItem
        """
        rentals = response.xpath(self.xpath_item_list)

        for rental in rentals:
            item = RentalItem()

            rental_url = self.__get_data(rental, self.xpath_url)
            if not rental_url:
                continue
            item['url'] = "{}/{}".format(self.domain, rental_url.strip())

            item['title'] = self.__get_data(rental, self.xpath_title)

            item['detail'] = self.__get_data(rental, self.xpath_detail)

            item['code'] = self.__get_data(rental, self.xpath_code)

            item['neighborhood'] = self.__get_data(
                rental, self.xpath_neighborhood)

            item['square_meters'] = self.__get_data(
                rental, self.xpath_square_meters)

            item['price'] = self.__get_data(rental, self.xpath_price)

            yield item

    def __get_data(self, rental_data, xpath):
        """Extract the data from the html with xpath.

        :param rental_data: parsed item from response
        :type rental_data: Response
        :param xpath: xpath query
        :type xpath: String
        :return: Result of the xpath query
        :rtype: String
        """
        data = rental_data.xpath(xpath).extract()
        if data:
            return data[0].strip()
        return ""
