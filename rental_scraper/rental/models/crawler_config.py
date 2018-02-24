# -*- coding: utf-8 -*-
"""Crawler Config model."""

from mongoengine import Document, StringField, URLField


class CrawlerConfig(Document):
    """Crawler config model."""

    meta = {'collection': 'rental_admin_crawlerconfig'}

    name = StringField(max_length=200, required=True, unique=True)
    domain = StringField(required=True)
    start_url = URLField(required=True)
    pagination_regex = StringField(required=True)

    xpath_item_list = StringField()
    xpath_neighborhood = StringField()
    xpath_square_meters = StringField()
    xpath_price = StringField()
    xpath_url = StringField()
    xpath_detail = StringField()
    xpath_title = StringField()
    xpath_code = StringField()
    xpath_next = StringField()
