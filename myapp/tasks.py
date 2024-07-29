import requests
import pandas as pd
from io import StringIO  # Correct import for StringIO
from .models import StockPrice
from celery import shared_task
from datetime import datetime, timedelta
from django.core.files.storage import default_storage
import json
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
    response = requests.get("https://query1.finance.yahoo.com/v7/finance/download/GOOG?period1=0&period2=9999999999&interval=1d&events=history")
    data = response.text
    df = pd.read_csv(StringIO(data))

    for _, row in df.iterrows():
        StockPrice.objects.update_or_create(
            date=row['Date'],
            defaults={
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume'],
                'ticker': 'GOOG'
            }
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


