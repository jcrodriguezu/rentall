# -*- coding: utf-8 -*-
"""Append filters to url tests."""

import unittest

from models.crawler_config import CrawlerConfig
from utils.url_utils import append_filters_to_url


class TestAppendFiltersToUrl(unittest.TestCase):
    """Test the filter handlers."""

    _url = "www.test_site.com?p1=1"
    _test_filters = {
        'city': '12345'
    }
    _empty_crawler_config_data = {
        'name': 'test_crawler'
    }

    def test_no_crawler_config(self):
        """Test no crawler_config provided."""
        result_url = append_filters_to_url(
            url=self._url, crawler_config=None, filters=self._test_filters)
        self.assertEqual(self._url, result_url)

    def test_no_filters_data(self):
        """Test no filters data provided."""
        crawler_config = CrawlerConfig(**self._empty_crawler_config_data)
        result_url = append_filters_to_url(
            url=self._url, crawler_config=crawler_config, filters=None)
        self.assertEqual(self._url, result_url)

    def test_url_filter_append_city(self):
        """Test append city filter to url."""
        crawler_config_data = self._empty_crawler_config_data.copy()
        crawler_config_data['filter_city'] = "city={city}"
        crawler_config = CrawlerConfig(**crawler_config_data)
        result_url = append_filters_to_url(
            url=self._url, crawler_config=crawler_config,
            filters=self._test_filters)
        url_to_compare = "{0}{1}".format(self._url, "&city=12345")
        self.assertEqual(url_to_compare, result_url)


if __name__ == '__main__':
    unittest.main()
