from django.db import models
import logging

logger = logging.getLogger(__name__)

class StockPrice(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    price_change_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_gainer = models.BooleanField(default=False)
    is_loser = models.BooleanField(default=False)

    class Meta:
        unique_together = ('date', 'ticker')
    
    def save(self, *args, **kwargs):
        # Ensure both open and close prices are set
        if self.open and self.close:
            try:
                # Calculate percentage change
                change_percentage = ((self.close - self.open) / self.open) * 100
                self.price_change_percentage = round(change_percentage, 2)

                # Determine if it's a gainer or loser
                self.is_gainer = change_percentage > 0
                self.is_loser = change_percentage < 0

                # Debug output
                logger.debug(f"Saving {self.ticker} - {self.date} with change_percentage: {self.price_change_percentage}, is_gainer: {self.is_gainer}, is_loser: {self.is_loser}")
            except Exception as e:
                logger.error(f"Error calculating price_change_percentage for {self.ticker} - {self.date}: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticker} - {self.date}"
