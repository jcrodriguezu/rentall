# -*- coding: utf-8 -*-
"""Rental crawler."""

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spiders.items import RentalItem
from utils.url_utils import append_filters_to_url


class EspacioUrbanoCrawler(CrawlSpider):
    """Espacio Urbano crawler."""

    name = "espacio_urbano_crawler"
    domain = 'espaciourbano.com'
    # start_urls = ['http://www.espaciourbano.com/BR_BuscarAnuncios_Resultado_Arriendo.asp?sNegocio=1&sZona=1&select2=M%E1s+recientes&rFotoanuncio=1&button=Buscar']
    start_urls = ['http://www.espaciourbano.com/BR_BuscarAnuncios_Resultado_Arriendo.asp?sNegocio=1&sZona=1&sCiudad=10012&sRango1=0&sRango2=999999999999&select2=M%E1s+recientes&rFotoanuncio=0&button=Buscar']

    pagination_regex = 'offset=[0-9]|[1-9][0-9]'
    xpath_item_list = '//div[@id="FrameBlanco"]/table/tr[3]/td[1]/table/tr/td'
    xpath_neighborhood = 'following::td[1]/table/tr/td[2]/div/span/text()'
    xpath_square_meters = 'following::td[1]/table/tr/td[3]/div/strong/text()'
    xpath_price = 'following::td[1]/table/tr/td[4]/div/strong[2]/text()'
    xpath_url = 'div/table/tr/td/a/@href'
    xpath_detail = 'div/table/tr/td/div[@class="FooterText"]/text()'
    xpath_title = 'div/table/tr/td/div[@class="FooterText"]/span[@class="style91"]/span/text()'
    xpath_code = 'following::td[1]/table/tr/td[1]/div/text()'
    xpath_next = '//div/span/a/img[@src="images/btn_siguiente.gif"]/ancestor::a'

    def __init__(self, crawler_config, filters=None, *args, **kwargs):
        """Rental Crawler constructor."""
        self.filters = filters
        self.crawler_config = crawler_config
        self.allowed_domains = [self.domain]
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
        super(EspacioUrbanoCrawler, self).__init__(*args, **kwargs)

#    def start_requests(self):
#        """Start the request to the urls.
#
#        :return: Request response
#        """
#        for url in self.start_urls:
#            final_url = append_filters_to_url(
#                url, self.crawler_config, self.filters
#            )
#            yield Request(final_url)

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
