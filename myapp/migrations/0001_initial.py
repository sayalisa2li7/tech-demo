# Generated by Django 2.2.12 on 2024-07-27 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockPriceData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('open', models.FloatField(null=True)),
                ('high', models.FloatField(null=True)),
                ('low', models.FloatField(null=True)),
                ('close', models.FloatField(null=True)),
                ('volume', models.BigIntegerField(null=True)),
                ('ticker', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'stock_prices',
            },
        ),
    ]
