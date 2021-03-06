import scrapy
import json

from datetime import datetime
from scrapers.settings import file_list_as_url


class CienCuadrasPageSpider(scrapy.Spider):
    name = "ciencuadras"
    current_page = 1
    max_page = 490

    # Set the headers here. The important part is "application/json"
    url = "https://api.ciencuadras.com/api/realestates"

    headers = {
        'authority': 'api.ciencuadras.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'application/json, text/plain, */*',
        'sec-fetch-dest': 'empty',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        'content-type': 'application/json',
        'origin': 'https://www.ciencuadras.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'accept-language': 'es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6'
    }

    body = {
        "criteria": [
            {"transactionType": "venta"},
            {"city": "medellin"}, {"cityReal": "Medellín"},
            {"countCityRepeat": 1}, {"offer": 0}
        ],
        "numberPaginator": current_page,
        "pathurl": "por-afinidad/venta/medellin",
        "status": False,
        "totalAsc": 0
    }

    def start_requests(self):
        yield scrapy.http.Request(
            self.url,
            method='POST',
            headers=self.headers,
            body=json.dumps(self.body)
        )

    def parse(self, response):
        parsed_json = json.loads(response.body)

        if not parsed_json.get('success', False):
            return

        data = parsed_json.get('data', None)
        if not data:
            return

        current_page = data.get('currentPage', 0)
        if current_page >= data.get('totalPages', 0) or \
                current_page >= self.max_page:
            return

        results = data.get('result', None)
        if not results:
            return

        filename = f'/scrapers-data/html/{self.name}-{current_page}.json'
        with open(filename, 'w') as f:
            f.write(json.dumps(results))
        self.log(f'Saved file {filename}')

        self.body['numberPaginator'] = data.get('nextPage', 0)
        yield scrapy.http.Request(
            self.url,
            method='POST',
            headers=self.headers,
            body=json.dumps(self.body)
        )


class CienCuadrasItemSpider(scrapy.Spider):
    """Cien cuadras item spider."""

    name = "ciencuadras_items"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = file_list_as_url('ciencuadras')

    def parse(self, response):
        items = json.loads(response.text)
        for item in items:
            parsed_item = {
                'neighborhood': item['barrio'],
                'square_meters': item['area_construida'],
                'price': item['precio_venta'],
                'location': item['localizacion']
            }

            yield parsed_item
