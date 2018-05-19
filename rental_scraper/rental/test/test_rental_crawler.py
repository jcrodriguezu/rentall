# -*- coding: utf-8 -*-
"""Rental crawler unit test."""

import unittest

from errors import CrawlerConfigNotProvidedError
from models.crawler_config import CrawlerConfig
from spiders.rental_crawler import RentalCrawler


class TestRentalCrawler(unittest.TestCase):
    """Test the rental crawler."""

    empty_string_config_data = {
        'name': "", 'domain': "", 'start_url': "",
        'pagination_regex': "", 'xpath_code': "",
        'xpath_detail': "", 'xpath_item_list': "",
        'xpath_neighborhood': "", 'xpath_next': "",
        'xpath_price': "", 'xpath_square_meters': "",
        'xpath_title': "", 'xpath_url': ""
    }

    def test_crawler_parse_no_config(self):
        """Test none config data."""
        with self.assertRaises(CrawlerConfigNotProvidedError):
            rental_crawler = RentalCrawler(
                crawler_config=None, filters=None)
            rental_crawler.parse(response=None)

    def test_empty_crawler_config(self):
        """Test empty config data object."""
        with self.assertRaises(
                ValueError, msg="RentalCrawler must have a name"):
            crawler_config = CrawlerConfig()
            rental_crawler = RentalCrawler(
                crawler_config=crawler_config, filters=None)
            rental_crawler.parse(response=None)

    def test_crawler_config_empty_string_params(self):
        """Test with empty strings config data."""
        with self.assertRaises(
                ValueError, msg="RentalCrawler must have a name"):
            crawler_config = CrawlerConfig(**self.empty_string_config_data)
            rental_crawler = RentalCrawler(
                crawler_config=crawler_config, filters=None)
            rental_crawler.parse_item(response=None)

    def test_crawler_config_with_name_param(self):
        """Test with just name config data."""
        with self.assertRaises(
                AttributeError,
                msg="'NoneType' object has no attribute 'xpath'"):
            data_with_name = self.empty_string_config_data.copy()
            data_with_name['name'] = "test"
            crawler_config = CrawlerConfig(**self.data_with_name)
            rental_crawler = RentalCrawler(
                crawler_config=crawler_config, filters=None)
            list(rental_crawler.parse_item(response=None))


if __name__ == '__main__':
    unittest.main()
