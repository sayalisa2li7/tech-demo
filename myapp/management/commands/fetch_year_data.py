from django.core.management.base import BaseCommand
import yfinance as yf
from myapp.models import StockPrice
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Fetch stock data for the last year for a predefined list of tickers and store it in the database'

    def handle(self, *args, **kwargs):
        # Predefined list of tickers
        tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
            'META', 'NVDA', 'NFLX', 'ADBE', 'INTC',
            'PYPL', 'CSCO', 'PEP', 'AVGO', 'COST',
            'TM', 'NKE', 'V', 'MA', 'JPM'
        ]  # Add more tickers as needed

        # Calculate the start date (one year ago)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)

        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                df = stock.history(start=start_date, end=end_date).reset_index()
                df['Date'] = df['Date'].dt.date

                # Save data to the database
                for _, row in df.iterrows():
                    # Check if data already exists
                    if not StockPrice.objects.filter(date=row['Date'], ticker=ticker).exists():
                        StockPrice.objects.create(
                            date=row['Date'],
                            ticker=ticker,
                            open=row['Open'],
                            high=row['High'],
                            low=row['Low'],
                            close=row['Close'],
                            volume=row['Volume']
                        )
                        self.stdout.write(self.style.SUCCESS(f'Successfully stored data for {ticker} on {row["Date"]}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Data already exists for {ticker} on {row["Date"]}'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Failed to fetch data for {ticker}: {e}'))
