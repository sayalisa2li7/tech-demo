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
# from .reports import generate_daily_report, generate_weekly_report, generate_monthly_report

# @shared_task
# def daily_report_task():
#     generate_daily_report()

# @shared_task
# def weekly_report_task():
#     generate_weekly_report()

# @shared_task
# def monthly_report_task():
#     generate_monthly_report()

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


# myapp/tasks.py

from celery import shared_task
from django.db.models import F, Subquery, OuterRef, FloatField, ExpressionWrapper
from .models import StockPrice, DailyClosingPriceReport, PriceChangePercentageReport, TopGainersLosersReport
from datetime import date, timedelta

@shared_task
def generate_daily_closing_price_report():
    data = StockPrice.objects.values('date', 'ticker').annotate(
        closing_price=F('close')
    ).order_by('date')

    for item in data:
        DailyClosingPriceReport.objects.update_or_create(
            date=item['date'],
            ticker=item['ticker'],
            defaults={'closing_price': item['closing_price']}
        )

@shared_task
def generate_price_change_percentage_report():
    first_close_subquery = StockPrice.objects.filter(
        ticker=OuterRef('ticker')
    ).order_by('date').values('close')[:1]

    last_close_subquery = StockPrice.objects.filter(
        ticker=OuterRef('ticker')
    ).order_by('-date').values('close')[:1]

    data = StockPrice.objects.values('ticker').annotate(
        first_close=Subquery(first_close_subquery, output_field=FloatField()),
        last_close=Subquery(last_close_subquery, output_field=FloatField()),
        price_change_percentage=ExpressionWrapper(
            (F('last_close') - F('first_close')) / F('first_close') * 100,
            output_field=FloatField()
        )
    ).order_by('-price_change_percentage')

    for item in data:
        PriceChangePercentageReport.objects.update_or_create(
            ticker=item['ticker'],
            defaults={
                'first_close': item['first_close'],
                'last_close': item['last_close'],
                'price_change_percentage': item['price_change_percentage']
            }
        )

@shared_task
def calculate_top_gainers_losers():
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Fetch prices for today and yesterday
    today_prices = StockPrice.objects.filter(date=today)
    yesterday_prices = StockPrice.objects.filter(date=yesterday)

    # Create dictionaries for easy lookup
    today_prices_dict = {price.ticker: price for price in today_prices}
    yesterday_prices_dict = {price.ticker: price for price in yesterday_prices}

    # Calculate top gainers and losers
    gainers = []
    losers = []

    for ticker, today_price in today_prices_dict.items():
        if ticker in yesterday_prices_dict:
            yesterday_price = yesterday_prices_dict[ticker]
            change_percentage = ((today_price.close - yesterday_price.close) / yesterday_price.close) * 100
            
            if change_percentage > 0:
                gainers.append({
                    'date': today,
                    'ticker': ticker,
                    'price_change_percentage': round(change_percentage, 2)
                })
            else:
                losers.append({
                    'date': today,
                    'ticker': ticker,
                    'price_change_percentage': round(change_percentage, 2)
                })

    # Clear existing data
    TopGainersLosersReport.objects.all().delete()

    # Save top gainers and losers to the database
    for gainer in gainers:
        TopGainersLosersReport.objects.create(
            date=gainer['date'],
            ticker=gainer['ticker'],
            price_change_percentage=gainer['price_change_percentage'],
            is_gainer=True
        )

    for loser in losers:
        TopGainersLosersReport.objects.create(
            date=loser['date'],
            ticker=loser['ticker'],
            price_change_percentage=loser['price_change_percentage'],
            is_gainer=False
        )


# def generate_report(start_date, end_date, report_type):
#     stock_data = StockPrice.objects.filter(date__range=[start_date, end_date])
#     df = pd.DataFrame(list(stock_data.values()))
    
#     if df.empty:
#         return

#     highest_value = df['close'].max()
#     lowest_value = df['close'].min()
    
#     df['price_change_percentage'] = df['close'].pct_change() * 100
#     top_gainers = df.nlargest(5, 'price_change_percentage')[['date', 'ticker', 'price_change_percentage']]
#     top_losers = df.nsmallest(5, 'price_change_percentage')[['date', 'ticker', 'price_change_percentage']]

#     report = {
#         'highest_value': highest_value,
#         'lowest_value': lowest_value,
#         'top_gainers': top_gainers.to_dict('records'),
#         'top_losers': top_losers.to_dict('records')
#     }

#     report_filename = f'{report_type}_report_{end_date.strftime("%Y-%m-%d")}.json'
#     with default_storage.open(report_filename, 'w') as f:
#         json.dump(report, f)


