# myapp/management/commands/update_metrics.py

from django.core.management.base import BaseCommand
from myapp.metrics import update_stock_metrics

class Command(BaseCommand):
    help = 'Update stock metrics for Prometheus'

    def handle(self, *args, **kwargs):
        update_stock_metrics()
        self.stdout.write(self.style.SUCCESS('Successfully updated stock metrics'))