
"""Finca raiz spider."""
import scrapy
from datetime import datetime


class EspacioUrbanoSpider(scrapy.Spider):
    """Finca raiz spider."""

    name = "fincaraiz"
    start_urls = [
        "https://www.fincaraiz.com.co/Vivienda/venta/medellin/?ad=30|0||||1||8,9,22,10,24,2|||55|5500006|||||||||||||||||||1||griddate%20desc||||||"
    ]
    count = 0

    def parse(self, response):
        # import pdb; pdb.set_trace()
        filename = f'/scrapers-data/{self.name}-{self.count}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        next_page_url = f"/Vivienda/venta/medellin/?ad=30|{self.count}||||1||8,9,22,10,24,2|||55|5500006|||||||||||||||||||1||griddate%20desc||||||"
        if next_page_url and self.count < 5:   # for testing, only download 10 pages
            self.count += 1
            yield response.follow(next_page_url, callback=self.parse)
