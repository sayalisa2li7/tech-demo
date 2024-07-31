from django.urls import path
from .views import StockListView, StockDetailView, daily_closing_price_report, price_change_percentage_report, top_gainers_losers_report
from .views import StockPriceViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import DailyClosingPriceReportView, PriceChangePercentageReportView, TopGainersLosersReportView

router = DefaultRouter()
router.register(r'stock-reports', StockPriceViewSet)

urlpatterns = [
    path('stocks/', StockListView.as_view(), name='stock-list'),
    path('stocks/<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
    path('reports/daily-closing-price/', views.daily_closing_price_report, name='daily_closing_price_report'),
    path('reports/price-change-percentage/', views.price_change_percentage_report, name='price_change_percentage_report'),
    path('reports/top-gainers-losers/', top_gainers_losers_report, name='top_gainers_losers_report'),
    path('', include(router.urls)), 
    path('daily-closing-price/', DailyClosingPriceReportView.as_view(), name='daily_closing_price_report'),
    path('price-change-percentage/', PriceChangePercentageReportView.as_view(), name='price_change_percentage_report'),
    path('top-gainers-losers/', TopGainersLosersReportView.as_view(), name='top_gainers_losers_report'),
    path('daily-report/', views.daily_report, name='daily_report'),
    path('weekly-report/', views.weekly_report, name='weekly_report'),
    path('monthly-report/', views.monthly_report, name='monthly_report'),
    path('metrics/', views.monthly_report, name='metrics'),
]
