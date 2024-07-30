# myapp/management/commands/generate_monthly_report.py
from django.core.management.base import BaseCommand
from myapp.models import StockPrice
import pandas as pd
from datetime import datetime, timedelta
import calendar

class Command(BaseCommand):
    help = 'Generate monthly stock report'

    def handle(self, *args, **kwargs):
        today = datetime.today().date()
        start_date = today.replace(day=1)
        end_date = (start_date + timedelta(days=calendar.monthrange(today.year, today.month)[1] - 1))
        df = pd.DataFrame(list(StockPrice.objects.filter(date__range=[start_date, end_date]).values()))

        if df.empty:
            self.stdout.write(self.style.WARNING('No data found for the given month'))
            return

        highest = df.loc[df['close'].idxmax()]
        lowest = df.loc[df['close'].idxmin()]

        report_data = {
            'start_date': start_date,
            'end_date': end_date,
            'highest': highest.to_dict(),
            'lowest': lowest.to_dict(),
        }

        # Print report to stdout (or save to a file or database as needed)
        self.stdout.write(self.style.SUCCESS(f'Monthly Report: {report_data}'))
