from django.urls import path
from .views import StockListView, StockDetailView, daily_closing_price_report, price_change_percentage_report, top_gainers_losers_report

urlpatterns = [
    path('stocks/', StockListView.as_view(), name='stock-list'),
    path('stocks/<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
    path('reports/daily-closing-price/', daily_closing_price_report, name='daily_closing_price_report'),
    path('reports/price-change-percentage/', price_change_percentage_report, name='price_change_percentage_report'),
    path('reports/top-gainers-losers/', top_gainers_losers_report, name='top_gainers_losers_report'),
    # path('reports/<str:report_type>/', get_report, name='get_report'),
]
