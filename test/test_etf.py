import yfinance as yf


etf = yf.Ticker("SPY")

# Get basic info
info = etf.info
print(info.get("currentPrice"))
print(info.get("shortName"))
print(info.get("sector"))

# Get price history (last 5 days)
history = etf.history(period="5d")
print(history)