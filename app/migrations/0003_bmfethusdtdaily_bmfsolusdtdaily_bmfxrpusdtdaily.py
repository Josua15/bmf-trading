# Generated by Django 5.1.5 on 2025-01-26 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_bmfdogeusdtdaily'),
    ]

    operations = [
        migrations.CreateModel(
            name='BmfEthUsdtDaily',
            fields=[
                ('unix', models.BigIntegerField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('symbol', models.CharField(max_length=255)),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume_eth', models.FloatField()),
                ('volume_usdt', models.FloatField()),
                ('trade_count', models.IntegerField()),
            ],
            options={
                'db_table': 'bmf_ethusdt_daily',
            },
        ),
        migrations.CreateModel(
            name='BmfSolUsdtDaily',
            fields=[
                ('unix', models.BigIntegerField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('symbol', models.CharField(max_length=255)),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume_sol', models.FloatField()),
                ('volume_usdt', models.FloatField()),
                ('trade_count', models.IntegerField()),
            ],
            options={
                'db_table': 'bmf_solusdt_daily',
            },
        ),
        migrations.CreateModel(
            name='BmfXrpUsdtDaily',
            fields=[
                ('unix', models.BigIntegerField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('symbol', models.CharField(max_length=255)),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume_xrp', models.FloatField()),
                ('volume_usdt', models.FloatField()),
                ('trade_count', models.IntegerField()),
            ],
            options={
                'db_table': 'bmf_xrpusdt_daily',
            },
        ),
    ]