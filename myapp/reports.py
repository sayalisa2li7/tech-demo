# # myapp/reports.py
# import pandas as pd
# from .models import StockPrice

# def generate_daily_report():
#     today = pd.Timestamp.now().normalize()
#     data = StockPrice.objects.filter(date=today)
#     df = pd.DataFrame(list(data.values()))
#     df['percentage_change'] = (df['close'] - df['open']) / df['open'] * 100
#     top_gainers = df.nlargest(3, 'percentage_change')[['date', 'ticker', 'percentage_change']]
#     top_losers = df.nsmallest(3, 'percentage_change')[['date', 'ticker', 'percentage_change']]
#     return {'top_gainers': top_gainers.to_dict(orient='records'), 'top_losers': top_losers.to_dict(orient='records')}

# def generate_weekly_report():
#     today = pd.Timestamp.now().normalize()
#     last_week = today - pd.DateOffset(weeks=1)
#     data = StockPrice.objects.filter(date__range=[last_week, today])
#     df = pd.DataFrame(list(data.values()))
#     df['percentage_change'] = (df['close'] - df['open']) / df['open'] * 100
#     top_gainers = df.nlargest(3, 'percentage_change')[['date', 'ticker', 'percentage_change']]
#     top_losers = df.nsmallest(3, 'percentage_change')[['date', 'ticker', 'percentage_change']]
#     return {'top_gainers': top_gainers.to_dict(orient='records'), 'top_losers': top_losers.to_dict(orient='records')}

# def generate_monthly_report():
#     today = pd.Timestamp.now().normalize()
#     last_month = today - pd.DateOffset(months=1)
#     data = StockPrice.objects.filter(date__range=[last_month, today])
#     df = pd.DataFrame(list(data.values()))
#     df['percentage_change'] = (df['close'] - df['open']) / df['open'] * 100
#     top_gainers = df.nlargest(3, 'percentage_change')[['date', 'ticker', 'percentage_change']]
#     top_losers = df.nsmallest(3, 'percentage_change')[['date', 'ticker', 'percentage_change']]
#     return {'top_gainers': top_gainers.to_dict(orient='records'), 'top_losers': top_losers.to_dict(orient='records')}
