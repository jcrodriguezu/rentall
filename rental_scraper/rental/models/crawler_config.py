# -*- coding: utf-8 -*-
"""Crawler Config model."""

from mongoengine import Document, StringField


class CrawlerConfig(Document):
    """Crawler config model."""

    meta = {'collection': 'rental_admin_crawlerconfig'}

    name = StringField(max_length=200, required=True, unique=True)

    filter_city = StringField()
    filter_neighborhood = StringField()
    filter_price = StringField()
    filter_square_meters = StringField()

    status = StringField()
