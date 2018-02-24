# -*- coding: utf-8 -*-

"""Crawler server."""
from klein import Klein
from controllers.crawler_controller import execute_chaining_crawler


app = Klein()


@app.route('/scrapy', methods=['GET'], branch=True)
def run_scrapy_crawler(request):
    """Web crawler with scrapy.

    :param request: end point request
    :type request: request
    :return: scraper execution results
    :rtype: String
    """
    request.setHeader('Content-Type', 'application/json')
    d = execute_chaining_crawler()
    return d


@app.route('/selenium', methods=['GET'], branch=True)
def run_selenium_crawler(request):
    """Web crawler with selenium.

    :param request: end point request
    :type request: request
    :return: scraper execution results
    :rtype: String
    """
    request.setHeader('Content-Type', 'application/json')
    return "Not implented yet."


if __name__ == '__main__':
    app.run("0.0.0.0", 8080)
