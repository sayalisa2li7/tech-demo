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
from django.utils.timezone import now
from django.core.files.storage import default_storage
from rest_framework import viewsets
from datetime import datetime, timedelta
# from .reports import generate_daily_report, generate_weekly_report, generate_monthly_report
import pandas as pd
from .serializers import StockPriceSerializer
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework import status
from .serializers import UserSerializer

# @login_required
def user_status(request):
    user = request.user
    return JsonResponse({
        'username': user.username,
        'is_authenticated': user.is_authenticated
    })

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    if not username or not password or not email:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password, email=email)
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response(UserSerializer(user).data)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
def metrics(request):
    registry = CollectorRegistry()
    gauge = Gauge('stock_price_change', 'Change in stock price', ['ticker'], registry=registry)

    # Example logic to update gauge with stock price changes
    for stock in StockPrice.objects.all():
        # Assuming price_change_percentage is a field in your model
        gauge.labels(ticker=stock.ticker).set(stock.price_change_percentage)

    data = generate_latest(registry)
    return HttpResponse(data, content_type='text/plain')


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

def weekly_report(request):
    today = datetime.today().date()
    start_date = today - timedelta(days=7)
    
    df = pd.DataFrame(list(StockPrice.objects.filter(date__gte=start_date, date__lte=today).values()))
    
    if df.empty:
        return JsonResponse({'error': 'No data found for the given period.'}, status=404)
    
    # Ensure 'close' column is of numeric type, handling conversion errors
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    
    # Drop rows where 'close' could not be converted to numeric
    df = df.dropna(subset=['close'])
    
    if df.empty:
        return JsonResponse({'error': 'No valid data found for the given period.'}, status=404)
    
    highest = df.loc[df['close'].idxmax()].to_dict()
    lowest = df.loc[df['close'].idxmin()].to_dict()
    
    report_data = {
        'start_date': str(start_date),
        'end_date': str(today),
        'highest': highest,
        'lowest': lowest,
    }

    return JsonResponse({'report': report_data})

def monthly_report(request):
    today = datetime.today().date()
    start_date = today - timedelta(days=30)
    
    df = pd.DataFrame(list(StockPrice.objects.filter(date__gte=start_date, date__lte=today).values()))
    
    if df.empty:
        return JsonResponse({'error': 'No data found for the given period.'}, status=404)
    
    # Ensure 'close' column is of numeric type, handling conversion errors
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    
    # Drop rows where 'close' could not be converted to numeric
    df = df.dropna(subset=['close'])
    
    if df.empty:
        return JsonResponse({'error': 'No valid data found for the given period.'}, status=404)
    
    highest = df.loc[df['close'].idxmax()].to_dict()
    lowest = df.loc[df['close'].idxmin()].to_dict()
    
    report_data = {
        'start_date': str(start_date),
        'end_date': str(today),
        'highest': highest,
        'lowest': lowest,
    }

    return JsonResponse({'report': report_data})


class DailyClosingPriceReportView(generics.ListAPIView):
    queryset = StockPrice.objects.all().order_by('date')
    serializer_class = StockPriceSerializer

class PriceChangePercentageReportView(generics.ListAPIView):
    queryset = StockPrice.objects.all().order_by('-price_change_percentage')
    serializer_class = StockPriceSerializer
# class PriceChangePercentageReportView(generics.ListAPIView):
#     serializer_class = StockPriceSerializer

#     def get_queryset(self):
#         period = self.request.query_params.get('period', 'daily')  # Default to 'daily'
#         today = timezone.now().date()

#         if period == 'daily':
#             return StockPrice.objects.filter(date=today).order_by('-price_change_percentage')
#         elif period == 'weekly':
#             start_of_week = today - timezone.timedelta(days=today.weekday())
#             return StockPrice.objects.filter(date__gte=start_of_week).order_by('-price_change_percentage')
#         elif period == 'monthly':
#             start_of_month = today.replace(day=1)
#             return StockPrice.objects.filter(date__gte=start_of_month).order_by('-price_change_percentage')
#         elif period == 'yearly':
#             start_of_year = today.replace(month=1, day=1)
#             return StockPrice.objects.filter(date__gte=start_of_year).order_by('-price_change_percentage')
#         else:
#             return StockPrice.objects.none()   

class TopGainersLosersReportView(generics.ListAPIView):
    serializer_class = StockPriceSerializer

    def get_queryset(self):
        is_gainer_str = self.request.query_params.get('is_gainer')
        
        if is_gainer_str is not None:
            # Convert the string to a boolean
            is_gainer = is_gainer_str.lower() in ['true', '1', 't', 'y', 'yes']
            return StockPrice.objects.filter(is_gainer=is_gainer).order_by('-price_change_percentage')
        
        return StockPrice.objects.all()

    
# class TopGainersLosersReportView(generics.ListAPIView):
#     serializer_class = StockPriceSerializer

#     def get_queryset(self):
#         today = now().date()
#         is_gainer_str = self.request.query_params.get('is_gainer')
        
#         if is_gainer_str is not None:
#             is_gainer = is_gainer_str.lower() in ['true', '1', 't', 'y', 'yes']
            
#             # Annotate with price change percentage
#             stocks = StockPrice.objects.filter(
#                 date__range=[today - timedelta(days=1), today]
#             ).annotate(
#                 price_change_percentage=ExpressionWrapper(
#                     (F('close') - F('open')) / F('open') * 100,
#                     output_field=FloatField()
#                 )
#             )

#             if is_gainer:
#                 # Order by price_change_percentage descending and slice the top 5 gainers
#                 stocks = stocks.filter(price_change_percentage__gt=0).order_by('-price_change_percentage')[:5]
#             else:
#                 # Order by price_change_percentage ascending to get the most negative values and slice the top 5 losers
#                 stocks = stocks.filter(price_change_percentage__lt=0).order_by('price_change_percentage')[:5]
            
#             return stocks
        
#         return StockPrice.objects.none()

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
