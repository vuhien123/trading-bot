import requests

def get_crypto_price(symbol="BTCUSDT"):
    # Dùng api3 thay vì api.binance.com
    urls = [
        "https://api3.binance.com/api/v3/klines",
        "https://api4.binance.com/api/v3/klines",
        "https://data-api.binance.vision/api/v3/klines",
    ]

    params = {
        "symbol": symbol,
        "interval": "1m",
        "limit": 100
    }

    for url in urls:
        try:
            res = requests.get(url, params=params, timeout=10)
            data = res.json()

            if not isinstance(data, list):
                print(f"API lỗi ({url}):", data)
                continue

            prices = [{
                'open':  float(candle[1]),
                'high':  float(candle[2]),
                'low':   float(candle[3]),
                'close': float(candle[4]),
            } for candle in data]

            return prices

        except Exception as e:
            print(f"Lỗi ({url}):", e)
            continue

    return []