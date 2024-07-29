from django.db import models

class StockPrice(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('ticker', 'date')
        ordering = ['-date']


# from django.db import models

# # myapp/models.py

# class StockPriceData(models.Model):
#     date = models.DateField()
#     open = models.FloatField(null=True)
#     high = models.FloatField(null=True)
#     low = models.FloatField(null=True)
#     close = models.FloatField(null=True)
#     volume = models.BigIntegerField(null=True)
#     ticker = models.CharField(max_length=10)

#     class Meta:
#         db_table = 'stock_prices_data'
