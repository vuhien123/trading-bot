import requests

def get_crypto_price(symbol="BTCUSDT"):
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": "1m",
        "limit": 100
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        # Debug kiểm tra data
        if not isinstance(data, list):
            print("API lỗi:", data)
            return []

        prices = [{
            'open':  float(candle[1]),
            'high':  float(candle[2]),
            'low':   float(candle[3]),
            'close': float(candle[4]),
        } for candle in data]

        return prices

    except Exception as e:
        print("Lỗi crypto:", e)
        return []