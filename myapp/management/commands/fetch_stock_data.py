# myapp/management/commands/fetch_stock_data.py

from django.core.management.base import BaseCommand
from myapp.tasks import fetch_stock_data

class Command(BaseCommand):
    help = 'Fetch stock data from Yahoo Finance'

    def handle(self, *args, **kwargs):
        try:
            fetch_stock_data.delay()
            self.stdout.write(self.style.SUCCESS('Successfully started the task to fetch stock data'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to start the task with Celery: {e}'))
            self.stderr.write(self.style.WARNING('Running the task directly...'))
            fetch_stock_data()


# from django.core.management.base import BaseCommand
# from myapp.tasks import fetch_stock_data

# class Command(BaseCommand):
#     help = 'Fetch stock data from Yahoo Finance API'

#     def handle(self, *args, **kwargs):
#         fetch_stock_data.delay()
#         self.stdout.write(self.style.SUCCESS('Successfully fetched stock data'))


# # myapp/management/commands/fetch_stock_data.py
# import yfinance as yf
# from django.core.management.base import BaseCommand
# from myapp.models import StockPriceData
# from django.utils.dateparse import parse_date

# class Command(BaseCommand):
#     help = 'Fetch stock data and store it in the database'

#     def add_arguments(self, parser):
#         parser.add_argument('ticker', type=str, help='Stock ticker symbol')

#     def handle(self, *args, **options):
#         ticker = options['ticker']
#         stock = yf.Ticker(ticker)
#         df = stock.history(period="1d").reset_index()
#         df['Date'] = df['Date'].dt.date

#         # Save data to the database
#         for _, row in df.iterrows():
#             StockPriceData.objects.update_or_create(
#                 date=row['Date'],
#                 ticker=ticker,
#                 defaults={
#                     'open': row['Open'],
#                     'high': row['High'],
#                     'low': row['Low'],
#                     'close': row['Close'],
#                     'volume': row['Volume']
#                 }
#             )
        
#         self.stdout.write(self.style.SUCCESS(f'Successfully stored data for {ticker}'))
