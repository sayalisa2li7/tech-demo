# myapp/management/commands/fetch_stock_data.py

from django.core.management.base import BaseCommand
import yfinance as yf
from myapp.models import StockPrice
from django.utils.dateparse import parse_date

class Command(BaseCommand):
    help = 'Fetch stock data for a predefined list of tickers and store it in the database'

    def handle(self, *args, **kwargs):
        # Predefined list of tickers
        tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
    'META', 'NVDA', 'NFLX', 'ADBE', 'INTC',
    'PYPL', 'CSCO', 'PEP', 'AVGO', 'COST',
    'TM', 'NKE', 'V', 'MA', 'JPM'
]  # Add more tickers as needed

        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                df = stock.history(period="1d").reset_index()
                df['Date'] = df['Date'].dt.date

                # Save data to the database
                for _, row in df.iterrows():
                    StockPrice.objects.update_or_create(
                        date=row['Date'],
                        ticker=ticker,
                        defaults={
                            'open': row['Open'],
                            'high': row['High'],
                            'low': row['Low'],
                            'close': row['Close'],
                            'volume': row['Volume']
                        }
                    )
                
                self.stdout.write(self.style.SUCCESS(f'Successfully stored data for {ticker}'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Failed to fetch data for {ticker}: {e}'))