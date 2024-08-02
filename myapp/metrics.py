# myapp/metrics.py

from prometheus_client import Gauge
from .models import StockPrice
from datetime import datetime, timedelta

# Define a custom gauge metric for stock value changes
stock_value_change_gauge = Gauge('stock_value_change_percentage', 'Percentage change in stock value', ['ticker'])

def update_stock_metrics():
    """Function to update the custom metrics."""
    stocks = StockPrice.objects.filter(date=datetime.today() - timedelta(days=1))  # Example filter
    for stock in stocks:
        try:
            percentage_change = (stock.close - stock.open) / stock.open * 100
            stock_value_change_gauge.labels(stock.ticker).set(percentage_change)
        except ZeroDivisionError:
            continue  # Handle cases where the stock open price is zero

