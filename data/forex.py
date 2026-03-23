import requests
import config

def get_gold_price():
    url = f"{config.TWELVE_BASE_URL}{config.TWELVE_ENDPOINT}"

    params = {
        "symbol": config.FOREX_SYMBOL,
        "interval": config.FOREX_INTERVAL,
        "outputsize": config.FOREX_OUTPUTSIZE,
        "apikey": config.TWELVE_API_KEY
    }

    try:
        res = requests.get(url, params=params)
        data = res.json()

        if "values" not in data:
            print("API lỗi:", data)
            return []

        values = data["values"]

        prices = [{
            'open':  float(candle['open']),
            'high':  float(candle['high']),
            'low':   float(candle['low']),
            'close': float(candle['close']),
        } for candle in values]

        # ✅ Đảo ngược thứ tự thời gian (mới nhất ở cuối)
        prices = prices[::-1]

        return prices

    except Exception as e:
        print("Lỗi forex:", e)
        return []