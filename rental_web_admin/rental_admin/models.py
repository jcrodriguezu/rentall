from djongo import models


class CrawlerConfig(models.Model):
    
    name = models.CharField(max_length=200, null=False, blank=False)
    domain = models.CharField(max_length=200, null=False, blank=False)
    start_url = models.URLField(max_length=200, null=False, blank=False)
    pagination_regex = models.CharField(max_length=200, null=False, blank=False)

    xpath_item_list = models.CharField(max_length=200)
    xpath_neighborhood = models.CharField(max_length=200)
    xpath_square_meters = models.CharField(max_length=200)
    xpath_price = models.CharField(max_length=200)
    xpath_url = models.CharField(max_length=200)
    xpath_detail = models.CharField(max_length=200)
    xpath_title = models.CharField(max_length=200)
    xpath_code = models.CharField(max_length=200)
    xpath_next = models.CharField(max_length=200)
