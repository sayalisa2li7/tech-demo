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


class DailyClosingPriceReport(models.Model):
    date = models.DateField()
    ticker = models.CharField(max_length=10)
    closing_price = models.FloatField()

    def __str__(self):
        return f"{self.ticker} - {self.date} - {self.closing_price}"

class PriceChangePercentageReport(models.Model):
    ticker = models.CharField(max_length=10)
    first_close = models.FloatField()
    last_close = models.FloatField()
    price_change_percentage = models.FloatField()

    def __str__(self):
        return f"{self.ticker} - {self.price_change_percentage}%"

class TopGainersLosersReport(models.Model):
    date = models.DateField()
    ticker = models.CharField(max_length=10)
    price_change_percentage = models.FloatField()
    is_gainer = models.BooleanField(null=True)

    class Meta:
        verbose_name = 'Top Gainers/Losers Report'
        verbose_name_plural = 'Top Gainers/Losers Reports'
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['ticker']),
            models.Index(fields=['is_gainer']),
        ]

    def __str__(self):
        return f"{'Gainer' if self.is_gainer else 'Loser'} - {self.ticker} on {self.date}"