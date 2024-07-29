from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from myapp.models import StockPrice

class Command(BaseCommand):
    help = 'Populates the database with dummy stock data for testing'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        # Clear existing data
        StockPrice.objects.all().delete()

        # Adding stock data for today
# Dummy data for yesterday
        StockPrice.objects.create(ticker="AAPL", date=yesterday, open=100, high=105, low=95, close=100, volume=100000)
        StockPrice.objects.create(ticker="TSLA", date=yesterday, open=200, high=210, low=195, close=200, volume=200000)
        StockPrice.objects.create(ticker="GOOGL", date=yesterday, open=300, high=315, low=290, close=300, volume=300000)

        # Dummy data for today
        StockPrice.objects.create(ticker="AAPL", date=today, open=104, high=110, low=100, close=104, volume=110000)
        StockPrice.objects.create(ticker="TSLA", date=today, open=194, high=200, low=190, close=194, volume=210000)  # Decrease
        StockPrice.objects.create(ticker="GOOGL", date=today, open=298, high=310, low=290, close=298, volume=320000)  # Decrease
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy stock data'))
