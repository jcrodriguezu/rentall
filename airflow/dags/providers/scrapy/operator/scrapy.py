from scrapy import signals
from scrapy.crawler import CrawlerProcess

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class ScrapyOperator(BaseOperator):
    """
    Initial version of the scrapy operator for apache airflow.
    Require the installation of scrapy (pip install scrapy)
    Current status:
        - Executes a scraper passing a scrapy spider class
        - Executes a scraper passing a scrapy spider class and callback to process each item
    Future work:
        - The operator should have the ability to execute scrapers in a scrapy project context to
          make use of the project configuration, pipelines and middlewares
    """
    @apply_defaults
    def __init__(
            self,
            scraper_cls,
            scraper_settings={},
            item_callback=None,
            return_items=False,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        if not scraper_cls:
            raise AirflowException('`scraper_cls` param must be class type')
        if item_callback and not callable(item_callback):
            raise AirflowException('`item_callback` param must be callable')

        self.item_callback = item_callback
        self.scraper_cls = scraper_cls
        self.return_items = return_items
        self.scraper_settings = scraper_settings
        self.results = []

    def item_scraped(self, item, response, spider):
        return self.results.append(item)

    def execute(self, context):
        process = CrawlerProcess(settings=self.scraper_settings)
        process.crawl(self.scraper_cls)
        if self.return_items:
            item_callback = self.item_callback if self.item_callback else self.item_scraped
            for p in process.crawlers:
                p.signals.connect(item_callback, signal=signals.item_scraped)
        process.start()
