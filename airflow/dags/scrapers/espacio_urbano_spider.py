
"""Espacio urbano spider."""
import os
import scrapy

from scrapy.utils.log import configure_logging


configure_logging(install_root_handler=False)


class EspacioUrbanoPageSpider(scrapy.Spider):
    """Espacio urbano spider."""

    name = "espaciourbano"
    start_urls = [
        "http://www.espaciourbano.com/BR_BuscarAnuncios_Resultado.asp?sZona=1&sCiudad=10035&sRango1=0&sRango2=999999999999&button=Buscar",
    ]
    next_page_xpath = "//img[@src='Imagenes/btn_siguiente.gif']/ancestor::a[1]/@href"
    count = 0

    def parse(self, response):
        self._save_file(response)
        next_page = response.xpath(self.next_page_xpath)[0].get()
        print(next_page)
        if next_page and self.count < 5:   # for testing, only download 10 pages
            self.count += 1
            yield response.follow(next_page, callback=self.parse)

    def _save_file(self, response):
        filename = f'/scrapers-data/html/{self.name}-{self.count}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')


class EspacioUrbanoItemSpider(scrapy.Spider):
    """Espacio urbano spider."""

    name = "espaciourbano_items"

    xpath_item_list = '//div[@id="FrameBlanco"]/table/tr[3]/td[1]/table/tr/td[@class and contains(concat(" ", normalize-space(@class), " "), " style33 ") and (@class and contains(concat(" ", normalize-space(@class), " "), " style100 "))]'
    xpath_neighborhood = 'following::td[1]/table/tr/td[2]/div/span/text()'
    xpath_square_meters = 'following::td[1]/table/tr/td[3]/div/strong/text()'
    xpath_price = 'following::td[1]/table/tr/td[4]/div/strong/text()'
    xpath_url = 'div/table/tr/td/a/@href'
    xpath_detail = 'div/table/tr/td/div[@class="FooterText"]/text()'
    xpath_title = 'div/table/tr/td/div[@class="FooterText"]/span[@class="style91"]/span/text()'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = get_file_list('espaciourbano')

    def parse(self, response):
        items = response.xpath(self.xpath_item_list)
        for item in items:
            # title = self.__get_data(item, self.xpath_title)
            # detail = self.__get_data(item, self.xpath_detail)
            neighborhood = self.__get_data(item, self.xpath_neighborhood)
            square_meters = self.__get_data(item, self.xpath_square_meters)
            price = self.__get_data(item, self.xpath_price, chars_to_remove=['$', ','])

            parsed_item = {
                # 'title': title,
                # 'detail': detail,
                'neighborhood': neighborhood,
                'square_meters': square_meters,
                'price': price
            }

            yield parsed_item

    def __get_data(self, rental_data, xpath, chars_to_remove=[]):
        data = rental_data.xpath(xpath).extract()
        data = data[0].strip() if data else ""
        if data and chars_to_remove:
            for the_char in chars_to_remove:
                data = data.replace(the_char, "")
        return data


def get_file_list(name, path="/scrapers-data/html/"):
    return [f"file:////{f.path}" for f in os.scandir(path=path)
            if f.is_file() and name in f.name]
