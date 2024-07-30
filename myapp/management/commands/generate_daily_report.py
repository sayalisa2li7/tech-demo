# myapp/management/commands/generate_daily_report.py
from django.core.management.base import BaseCommand
from myapp.models import StockPrice
import pandas as pd
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate daily stock report'

    def handle(self, *args, **kwargs):
        today = datetime.today().date()
        start_date = today - timedelta(days=1)
        df = pd.DataFrame(list(StockPrice.objects.filter(date=start_date).values()))

        if df.empty:
            self.stdout.write(self.style.WARNING('No data found for the given date'))
            return

        highest = df.loc[df['close'].idxmax()]
        lowest = df.loc[df['close'].idxmin()]

        report_data = {
            'date': start_date,
            'highest': highest.to_dict(),
            'lowest': lowest.to_dict(),
        }

        # Print report to stdout (or save to a file or database as needed)
        self.stdout.write(self.style.SUCCESS(f'Daily Report: {report_data}'))
