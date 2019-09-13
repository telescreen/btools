from django.db import models

class Company(models.Model):
    """ A company store all company's general information """
    quote = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=500)
    summary = models.TextField()
    industry = models.CharField(max_length=100)


class StockTimeStamp(models.Model):
    """ A Stock Timestamp stores index for a specific date """
    quote = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField(unique=True)


class DailyStockPrice(models.Model):
    """ A Stock Data stores various information about  """
    quote = models.ForeignKey(Company, to_field='quote', on_delete=models.CASCADE)
    date = models.ForeignKey(StockTimeStamp, to_field='date', on_delete=models.CASCADE)
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()
    adjusted_close_price = models.FloatField()

    def __str__(self):
        return 'PriceData<{},{},{},{},{},{},{},{}>'.format(
            self.quote,
            self.date,
            self.open_price,
            self.high_price,
            self.low_price,
            self.close_price,
            self.volume,
            self.adjusted_close_price
        )