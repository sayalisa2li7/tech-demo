from rest_framework import generics
from .models import StockPrice
from .serializers import StockPriceSerializer
from datetime import timedelta
from django.http import JsonResponse
from datetime import datetime 
from .models import StockPrice
from rest_framework import viewsets
from datetime import datetime, timedelta
import pandas as pd
from .serializers import StockPriceSerializer
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import UserSerializer
from django.http import HttpResponse
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from .models import StockPrice

def stock_price_metrics(request):
    registry = CollectorRegistry()
    
    # Define your custom metrics
    stock_price_gauge = Gauge('stock_price_change_percentage', 
                              'Percentage change in stock price',
                              ['ticker'],
                              registry=registry)
    
    # Fetch stock data and update metrics
    stock_prices = StockPrice.objects.all()
    for stock in stock_prices:
        stock_price_gauge.labels(ticker=stock.ticker).set(stock.price_change_percentage or 0)
    
    # Generate the metrics output
    metrics = generate_latest(registry).decode('utf-8')
    
    return HttpResponse(metrics, content_type='text/plain; version=0.0.4; charset=utf-8')

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
