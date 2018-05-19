# -*- coding: utf-8 -*-
"""Registry of crawlers."""

from spiders.espacio_urbano_crawler import EspacioUrbanoCrawler


CRAWLER_REGISTER = {
    'espacio_urbano_crawler': EspacioUrbanoCrawler
}
