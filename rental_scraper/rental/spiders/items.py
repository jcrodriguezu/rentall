# -*- coding: utf-8 -*-
"""scraped items model."""

from scrapy.item import Field, Item


class RentalItem(Item):
    """Definition of the item fields required by the web crawler."""

    title = Field()
    detail = Field()
    neighborhood = Field()
    square_meters = Field()
    price = Field()
    code = Field()
    url = Field()
