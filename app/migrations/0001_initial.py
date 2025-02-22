# Generated by Django 5.1.5 on 2025-01-25 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BmfBtcUsdtDaily',
            fields=[
                ('unix', models.BigIntegerField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('symbol', models.CharField(max_length=255)),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume_btc', models.FloatField()),
                ('volume_usdt', models.FloatField()),
                ('trade_count', models.IntegerField()),
            ],
            options={
                'db_table': 'bmf_btcusdt_daily',
            },
        ),
    ]
