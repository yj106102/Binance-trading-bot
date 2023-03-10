# Generated by Django 4.1.6 on 2023-03-05 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradinghelper', '0002_tradingstrategyrecord_number_of_trades_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RSIRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strategy_type', models.CharField(max_length=10)),
                ('symbol', models.CharField(max_length=10)),
                ('benefit', models.FloatField(default=0)),
                ('open_rsi_threshold', models.FloatField(default=30)),
                ('close_rsi_threshold', models.FloatField(default=50)),
            ],
        ),
        migrations.DeleteModel(
            name='TradingStrategyRecord',
        ),
    ]
