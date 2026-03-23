last_signal = None
fib_high = None
fib_low = None

def trading_logic(df):
    global last_signal, fib_high, fib_low

    if len(df) < 11:
        return "HOLD", None, None, 0

    prev = df.iloc[-2]
    curr = df.iloc[-1]
    c2 = df.iloc[-3]  # nến cách 2

    # =====================
    # 🔥 GAINZ ALGO V2
    # =====================
    stable_candle = abs(curr['close'] - curr['open']) / (curr['tr'] + 1e-9) > 0.7
    rsi = curr['rsi']

    bullish_engulfing = (
        prev['close'] < prev['open'] and
        curr['close'] > curr['open'] and
        curr['close'] > prev['open']
    )
    bearish_engulfing = (
        prev['close'] > prev['open'] and
        curr['close'] < curr['open'] and
        curr['close'] < prev['open']
    )

    rsi_below = rsi < 80
    rsi_above = rsi > 20
    decrease_over = curr['close'] < df.iloc[-11]['close']
    increase_over = curr['close'] > df.iloc[-11]['close']

    bull_gainz = bullish_engulfing and stable_candle and rsi_below and decrease_over
    bear_gainz = bearish_engulfing and stable_candle and rsi_above and increase_over

    # =====================
    # 🔥 VICTORY PRO — ALMA Cross
    # =====================
    alma_buy  = prev['alma1'] < prev['alma2'] and curr['alma1'] > curr['alma2']  # crossover
    alma_sell = prev['alma1'] > prev['alma2'] and curr['alma1'] < curr['alma2']  # crossunder

    # =====================
    # 🔥 FVG
    # =====================
    fvg_buy  = c2['low'] > curr['high']   # low[2] > high[0]
    fvg_sell = c2['high'] < curr['low']   # high[2] < low[0]

    # =====================
    # 🚀 COMBINE
    # =====================
    confidence = 0

    # BUY: cần ALMA cross + ít nhất 1 trong (gainz hoặc fvg)
    bull = alma_buy and (bull_gainz or fvg_buy) and last_signal != "buy"

    # SELL: cần ALMA cross + ít nhất 1 trong (gainz hoặc fvg)
    bear = alma_sell and (bear_gainz or fvg_sell) and last_signal != "sell"

    # tính confidence
    if alma_buy or alma_sell:
        confidence += 40
    if bull_gainz or bear_gainz:
        confidence += 40
    if fvg_buy or fvg_sell:
        confidence += 20

    # =====================
    # 💰 TP / SL (RRR 1:2)
    # =====================
    signal = "HOLD"
    tp = None
    sl = None

    if bull:
        last_signal = "buy"
        dist = curr['atr']
        tp = round(curr['close'] + dist * 2, 2)
        sl = round(curr['close'] - dist, 2)
        signal = "BUY"

        # Fibonacci
        fib_low = curr['low']

    elif bear:
        last_signal = "sell"
        dist = curr['atr']
        tp = round(curr['close'] - dist * 2, 2)
        sl = round(curr['close'] + dist, 2)
        signal = "SELL"

        # Fibonacci
        fib_high = curr['high']

    return signal, tp, sl, confidence


def generate_signal(rsi, df):
    signal, tp, sl, confidence = trading_logic(df)

    if signal != "HOLD":
        return f"{signal} | TP: {tp} | SL: {sl} | Confidence: {confidence}%"
    return "HOLD"