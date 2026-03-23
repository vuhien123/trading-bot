# binace
binace_base_ulr = [ 
     "https://api.binance.com",
    "https://api1.binance.com",
    "https://api2.binance.com"
]

binace_klines_endpoint = "/api/v3/klines"

#trading 

symbol = "BTCUSDT"
interval = "1m"
limit = 1000

# discord
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1485479037332623370/p7xOmF64Jz2-hzyUh9_LHcr74XcZCiQWORc5fPjzvktszKcz1DpDXFy7Bia-qwYFdWxr"
#settings
request_timeout = 3
debug = True

TWELVE_API_KEY = "7c924d796d83465cb2907d6ffe04fc5f"
TWELVE_BASE_URL = "https://api.twelvedata.com"
TWELVE_ENDPOINT = "/time_series"
FOREX_SYMBOL = "XAU/USD"
FOREX_INTERVAL = "1min"
FOREX_OUTPUTSIZE = 1000

def parse_klines(raw):
    return [{
        'open':  float(k[1]),
        'high':  float(k[2]),
        'low':   float(k[3]),
        'close': float(k[4]),
    } for k in raw]