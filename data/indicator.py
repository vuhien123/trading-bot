import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange


def alma(series, window=10, offset=0.85, sigma=6):
    m = offset * (window - 1)
    s = window / sigma
    weights = np.array([
        np.exp(-((i - m) ** 2) / (2 * s * s)) for i in range(window)
    ])
    weights /= weights.sum()
    return series.rolling(window).apply(lambda x: np.sum(weights * x), raw=True)


def calculate_indicators(prices):
    if not prices:
        print("⚠️ prices rỗng hoặc None!")
        return None, None

    df = pd.DataFrame(prices)
    df = df[['open', 'high', 'low', 'close']].astype(float)

    # ALMA
    df['alma1'] = alma(df['close'], 10)
    df['alma2'] = alma(df['close'], 20)
    df['alma3'] = alma(df['close'], 50)  # ✅ thêm alma3

    # RSI
    df['rsi'] = RSIIndicator(df['close'], window=14).rsi()

    # ATR
    df['atr'] = AverageTrueRange(
        df['high'], df['low'], df['close'], window=14
    ).average_true_range()

    # TRUE RANGE
    df['tr'] = df['high'] - df['low']

    # STABLE
    df['stable'] = abs(df['close'] - df['open']) / (df['tr'] + 1e-9) > 0.7

    # ENGULF
    df['bullish_engulf'] = (
        (df['close'].shift(1) < df['open'].shift(1)) &
        (df['close'] > df['open']) &
        (df['close'] > df['open'].shift(1))  # ✅ thêm điều kiện Pine Script
    )
    df['bearish_engulf'] = (
        (df['close'].shift(1) > df['open'].shift(1)) &
        (df['close'] < df['open']) &
        (df['close'] < df['open'].shift(1))  # ✅ thêm điều kiện Pine Script
    )

    # TREND
    df['decrease'] = df['close'] < df['close'].shift(10)
    df['increase'] = df['close'] > df['close'].shift(10)

    return df['rsi'], df