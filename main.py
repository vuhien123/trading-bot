import time

from data.crypto import get_crypto_price
from data.forex import get_gold_price
from data.indicator import calculate_indicators
from data.logic import generate_signal
from init import send_discord


def run_bot():
    # --- BTC ---
    btc_prices = get_crypto_price("BTCUSDT")
    rsi, df = calculate_indicators(btc_prices)

    # DEBUG
    print("=== BTC DATA ===")
    print(f"Số nến: {len(df)}")
    print(f"Mẫu OHLC:\n{df[['open','high','low','close']].tail(3)}")
    print(f"Indicators:\n{df[['bullish_engulf','bearish_engulf','stable','alma1','alma2']].tail(3)}")
    print(f"RSI cuối: {df['rsi'].iloc[-1]:.2f}")
    print(f"ATR cuối: {df['atr'].iloc[-1]:.5f}")

    if rsi is None or df is None:
        print("❌ Không tính được indicators BTC, bỏ qua vòng này.")
        return
    signal_btc = generate_signal(rsi, df)  # ✅ thêm dòng này

    # --- Gold ---
  # --- Gold ---
    gold_prices = get_gold_price()
    rsi_g, df_g = calculate_indicators(gold_prices)

    # DEBUG GOLD
    print("=== GOLD DATA ===")
    print(f"Số nến: {len(df_g)}")
    print(f"Mẫu OHLC:\n{df_g[['open','high','low','close']].tail(3)}")
    print(f"Indicators:\n{df_g[['bullish_engulf','bearish_engulf','stable','alma1','alma2']].tail(3)}")
    print(f"RSI cuối: {df_g['rsi'].iloc[-1]:.2f}")
    print(f"ATR cuối: {df_g['atr'].iloc[-1]:.5f}")

    if rsi_g is None or df_g is None:
        print("❌ Không tính được indicators Gold, bỏ qua vòng này.")
        return

    signal_gold = generate_signal(rsi_g, df_g)

    # --- Gửi Discord ---
    message = f"""
📊 SIGNAL

BTC: {signal_btc}
XAU/USD: {signal_gold}
"""
    print(message)
    send_discord(message)


if __name__ == "__main__":
    while True:
        run_bot()
        time.sleep(300)