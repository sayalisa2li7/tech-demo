from rest_framework import generics
from .models import StockPrice
from .serializers import StockPriceSerializer
from datetime import timedelta, date
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime 
from django.db.models import Subquery, OuterRef, FloatField, ExpressionWrapper
from django.shortcuts import render
from django.db.models import Avg, Max, Min, F, ExpressionWrapper, FloatField
from .models import StockPrice
import calendar

from django.core.files.storage import default_storage
from rest_framework import viewsets
from datetime import datetime, timedelta
# from .reports import generate_daily_report, generate_weekly_report, generate_monthly_report
import pandas as pd
from .serializers import StockPriceSerializer

def daily_report(request):
    today = datetime.today().date()
    start_date = today - timedelta(days=1)
    
    # Retrieve data and convert it to a DataFrame
    data = list(StockPrice.objects.filter(date=start_date).values())
    df = pd.DataFrame(data)
    
    # Check if the DataFrame is empty
    if df.empty:
        return JsonResponse({'error': 'No data found for the given date.'}, status=404)
    
    # Ensure the 'close' column is numeric, coercing errors to NaN
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    
    # Drop rows with NaN values in 'close' column
    df = df.dropna(subset=['close'])
    
    # If the DataFrame is empty after cleaning, return an error
    if df.empty:
        return JsonResponse({'error': 'No valid data found for the given date.'}, status=404)

    # Find the rows with the highest and lowest 'close' values
    highest = df.loc[df['close'].idxmax()].to_dict()
    lowest = df.loc[df['close'].idxmin()].to_dict()
    
    # Prepare the report data
    report_data = {
        'date': str(start_date),
        'highest': highest,
        'lowest': lowest,
    }

    # Return the report as JSON
    return JsonResponse({'report': report_data})

class DailyClosingPriceReportView(generics.ListAPIView):
    queryset = StockPrice.objects.all().order_by('date')
    serializer_class = StockPriceSerializer

class PriceChangePercentageReportView(generics.ListAPIView):
    queryset = StockPrice.objects.all().order_by('-price_change_percentage')
    serializer_class = StockPriceSerializer

class TopGainersLosersReportView(generics.ListAPIView):
    serializer_class = StockPriceSerializer

    def get_queryset(self):
        is_gainer_str = self.request.query_params.get('is_gainer')
        
        if is_gainer_str is not None:
            # Convert the string to a boolean
            is_gainer = is_gainer_str.lower() in ['true', '1', 't', 'y', 'yes']
            return StockPrice.objects.filter(is_gainer=is_gainer).order_by('-price_change_percentage')
        
        return StockPrice.objects.all()

class StockPriceViewSet(viewsets.ModelViewSet):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

class StockListView(generics.ListCreateAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

class StockDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

# views.py

from django.shortcuts import render
from .models import StockPrice


def daily_closing_price_report(request):
    data = StockPrice.objects.all().order_by('date')
    return render(request, 'reports/daily_closing_price.html', {'data': data})

def price_change_percentage_report(request):
    data = StockPrice.objects.exclude(price_change_percentage__isnull=True).order_by('-price_change_percentage')
    return render(request, 'reports/price_change_percentage.html', {'data': data})

def top_gainers_losers_report(request):
    gainers = StockPrice.objects.filter(is_gainer=True).order_by('-price_change_percentage')
    losers = StockPrice.objects.filter(is_loser=True).order_by('price_change_percentage')
    
    context = {
        'top_gainers': gainers,
        'top_losers': losers
    }
    return render(request, 'reports/top_gainers_losers.html', context)
