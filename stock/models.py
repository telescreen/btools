""" Data Model for Stock Application """

from datetime import datetime
from django.db import models

class Company(models.Model):
    """ A company store all company's general information """
    class Meta:
        indexes = [
            models.Index(fields=['quote'], name='quote_idx')
        ]

    quote = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=500)
    summary = models.TextField()
    industry = models.CharField(max_length=100)


class StockTimeStamp(models.Model):
    """ A Stock Timestamp stores index for a specific date """
    quote = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    processed = models.BooleanField(default=False)


class DailyStockPrice(models.Model):
    """ A Stock Data stores various information about  """
    quote = models.ForeignKey(Company, to_field='quote', on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()
    adjusted_price = models.FloatField()

    def __str__(self):
        """ Return String to Price Data """
        return 'PriceData<{},{},{},{},{},{},{},{}>'.format(
            self.quote,
            self.date,
            self.open_price,
            self.high_price,
            self.low_price,
            self.close_price,
            self.volume,
            self.adjusted_price
        )
