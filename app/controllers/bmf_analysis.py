import pandas as pd
import numpy as np
from django.http import JsonResponse
from ..models import BmfBtcUsdtDaily

def load_data_from_db():
    queryset = BmfBtcUsdtDaily.objects.all().values(
        "unix", "date", "symbol", "open", "high", "low", "close", "volume_btc", "volume_usdt", "trade_count"
    )
    df = pd.DataFrame.from_records(queryset)
    return df

def calculate_moving_averages(df, col="close", intervals=range(5, 55, 5)):
    for period in intervals:
        df[f"MA_{period}"] = df[col].rolling(window=period).mean()
        df[f"MA_{period}_Derivative"] = df[f"MA_{period}"].diff() / df.index.to_series().diff()

def calculate_emas(df, col="close", intervals=range(5, 55, 5)):
    for period in intervals:
        df[f"EMA_{period}"] = df[col].ewm(span=period, adjust=False).mean()
        df[f"EMA_{period}_Derivative"] = df[f"EMA_{period}"].diff() / df.index.to_series().diff()

def calculate_rsi(df, col="close", period=14):
    delta = df[col].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    df[f"RSI_{period}"] = 100 - (100 / (1 + rs))

def calculate_atr(df, period=20):
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df[f"ATR_{period}"] = true_range.rolling(window=period).mean()

def calculate_macd(df, col="close", slow=26, fast=12, signal=9):
    ema_fast = df[col].ewm(span=fast, adjust=False).mean()
    ema_slow = df[col].ewm(span=slow, adjust=False).mean()
    
    df["MACD"] = ema_fast - ema_slow
    df["Signal_Line"] = df["MACD"].ewm(span=signal, adjust=False).mean()

def calculate_bollinger_bands(df, col="close", intervals=[10, 20, 30, 40, 50], k=2):
    for n in intervals:
        rolling_mean = df[col].rolling(window=n).mean()
        rolling_std = df[col].rolling(window=n).std()
        
        df[f"BB_Upper_{n}"] = rolling_mean + (k * rolling_std)
        df[f"BB_Lower_{n}"] = rolling_mean - (k * rolling_std)

def triple_barrier_labeling(df, col="close", tp_thresh=0.05):
    labels = np.zeros(len(df))
    for i in range(len(df)):
        entry_price = df[col].iloc[i]
        atr_value = df[f"ATR_20"].iloc[i]
        tp_target = entry_price + atr_value

        future_prices = df[col].iloc[i+1:]
        horizon = (future_prices >= tp_target).idxmax() if (future_prices >= tp_target).any() else len(df) - 1
        future_prices = df[col].iloc[i+1:horizon+1]

        price_changes = (future_prices - entry_price) / entry_price
        sl_thresh = tp_thresh / 3

        hit_tp = (price_changes >= tp_thresh).any()
        hit_sl = (price_changes <= -sl_thresh).any()

        if hit_tp:
            labels[i] = 1
        elif hit_sl:
            labels[i] = -1
        else:
            labels[i] = 0

    df["Label"] = labels
    return df

def process_ohlcv():
    df = load_data_from_db()
    
    calculate_moving_averages(df)
    calculate_emas(df)
    calculate_rsi(df)
    calculate_atr(df)
    calculate_macd(df)
    calculate_bollinger_bands(df)
    triple_barrier_labeling(df)
    
    return df

def ohlcv_analysis_view(request):
    df = process_ohlcv()
    df.fillna(0, inplace=True)
    return JsonResponse(df.to_dict(orient="records"), safe=False)
