# myapp/metrics.py

from prometheus_client import Gauge, generate_latest
from django.http import HttpResponse

# Define your metrics
stock_value_change_gauge = Gauge('stock_value_change', 'Stock value change percentage', ['ticker'])

def metrics_view(request):
    # Example: Set the value for a specific stock ticker
    stock_value_change_gauge.labels(ticker='AAPL').set(1.5)  # Replace with actual logic to fetch stock changes

    return HttpResponse(generate_latest(), content_type='text/plain')
