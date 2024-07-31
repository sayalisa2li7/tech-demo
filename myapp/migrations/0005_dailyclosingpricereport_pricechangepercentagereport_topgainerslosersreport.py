# Generated by Django 3.2.25 on 2024-07-30 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_stockprice_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyClosingPriceReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('ticker', models.CharField(max_length=10)),
                ('closing_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PriceChangePercentageReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('first_close', models.FloatField()),
                ('last_close', models.FloatField()),
                ('price_change_percentage', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TopGainersLosersReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('ticker', models.CharField(max_length=10)),
                ('price_change_percentage', models.FloatField()),
                ('report_type', models.CharField(choices=[('gainer', 'Gainer'), ('loser', 'Loser')], max_length=6)),
            ],
        ),
    ]