from djongo import models


class CrawlerConfig(models.Model):
    """
    Model definition for the crawler configuration.
    """

    name = models.CharField(max_length=200, null=False, blank=False)

    # parameters allowed in the url filter
    filter_city = models.CharField(max_length=100, null=True, blank=True)
    filter_neighborhood = models.CharField(
        max_length=100, null=True, blank=True)
    filter_price = models.CharField(max_length=100, null=True, blank=True)
    filter_square_meters = models.CharField(
        max_length=100, null=True, blank=True)

    status = models.CharField(
        max_length=50, null=False, blank=False, default="ACTIVE")

    def __str__(self):
        return '{0}'.format(self.name)
