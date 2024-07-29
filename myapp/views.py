from rest_framework import generics
from .models import StockPrice
from .serializers import StockPriceSerializer
from datetime import timedelta, date
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime 

from django.shortcuts import render
from django.db.models import Avg, Max, Min, F, ExpressionWrapper, FloatField
from .models import StockPrice

from django.core.files.storage import default_storage
import json
from datetime import datetime, timedelta
# from .reports import generate_daily_report, generate_weekly_report, generate_monthly_report


class StockListView(generics.ListCreateAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

class StockDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

def daily_closing_price_report(request):
    data = StockPrice.objects.values('date', 'ticker').annotate(
        closing_price=F('close')
    ).order_by('date')
    return render(request, 'reports/daily_closing_price.html', {'data': data})

from django.db.models import Subquery, OuterRef, FloatField, ExpressionWrapper

def price_change_percentage_report(request):
    # Subquery to get the first close price
    first_close_subquery = StockPrice.objects.filter(
        ticker=OuterRef('ticker')
    ).order_by('date').values('close')[:1]

    # Subquery to get the last close price
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

    return render(request, 'reports/price_change_percentage.html', {'data': data})


def top_gainers_losers_report(request):
    today = date.today()
    yesterday = today - timedelta(days=1)

    yesterday_prices = StockPrice.objects.filter(date=yesterday)
    today_prices = StockPrice.objects.filter(date=today)

    top_gainers = []
    top_losers = []

    for stock in today_prices:
        try:
            yesterday_price = yesterday_prices.get(ticker=stock.ticker)
            change_percentage = ((stock.close - yesterday_price.close) / yesterday_price.close) * 100
            if change_percentage > 0:
                top_gainers.append({
                    'date': stock.date,
                    'ticker': stock.ticker,
                    'price_change_percentage': round(change_percentage, 2)
                })
            else:
                top_losers.append({
                    'date': stock.date,
                    'ticker': stock.ticker,
                    'price_change_percentage': round(change_percentage, 2)
                })
        except StockPrice.DoesNotExist:
            continue

    context = {
        'top_gainers': top_gainers,
        'top_losers': top_losers
    }
    return render(request, 'reports/top_gainers_losers.html', context)

# def daily_closing_price_report(request):
#     report = generate_daily_report()
#     return JsonResponse(report)

# def price_change_percentage_report(request):
#     report = generate_daily_report()
#     return JsonResponse(report)

# def top_gainers_losers_report(request):
#     report = generate_daily_report()
#     return JsonResponse(report)

# def get_report(request, report_type):
#     if report_type == 'daily':
#         report = generate_daily_report()
#     elif report_type == 'weekly':
#         report = generate_weekly_report()
#     elif report_type == 'monthly':
#         report = generate_monthly_report()
#     else:
#         return JsonResponse({'error': 'Report not found'})
    
#     return JsonResponse(report)
        