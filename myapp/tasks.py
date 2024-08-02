import requests
import pandas as pd
from io import StringIO  # Correct import for StringIO
from .models import StockPrice
from celery import shared_task
from datetime import datetime, timedelta
from django.core.files.storage import default_storage
import json
from celery import shared_task
import yfinance as yf
from myapp.models import StockPrice
from django.core.management import call_command
from .metrics import update_stock_metrics

@shared_task
def update_metrics_task():
    update_stock_metrics()

@shared_task
def generate_daily_report():
    call_command('generate_daily_report')

@shared_task
def fetch_stock_data():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "INTC", "PYPL", "CSCO", "PEP", "AVGO", "COST", "TM", "NKE", "V", "MA", "JPM"]

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
            print(f'Successfully stored data for {ticker}')
        except Exception as e:
            print(f"Failed to get ticker '{ticker}' reason: {e}")

