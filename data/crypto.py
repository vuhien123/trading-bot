import requests

def get_crypto_price(symbol="BTCUSDT"):
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": "1m",
        "limit": 100
    }

    res = requests.get(url, params=params)
    data = res.json()

    # ✅ Lấy đủ OHLC thật
    prices = [{
        'open':  float(candle[1]),
        'high':  float(candle[2]),
        'low':   float(candle[3]),
        'close': float(candle[4]),
    } for candle in data]

    return prices