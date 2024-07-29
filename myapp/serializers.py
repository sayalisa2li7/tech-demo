from rest_framework import serializers
from .models import StockPrice

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = '__all__'
