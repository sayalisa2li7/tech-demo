# Generated by Django 3.2.25 on 2024-07-30 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20240730_0625'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DailyClosingPriceReport',
        ),
        migrations.DeleteModel(
            name='PriceChangePercentageReport',
        ),
        migrations.DeleteModel(
            name='TopGainersLosersReport',
        ),
        migrations.AlterModelOptions(
            name='stockprice',
            options={},
        ),
        migrations.AddField(
            model_name='stockprice',
            name='is_gainer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stockprice',
            name='is_loser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stockprice',
            name='price_change_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='stockprice',
            unique_together={('date', 'ticker')},
        ),
    ]