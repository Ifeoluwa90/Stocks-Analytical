import yfinance as yf

stock = yf.Ticker("AAPL")

# Get basic info
info = stock.info
print(info["currentPrice"])
print(info["shortName"])
print(info["sector"])

# Get price history (last 5 days)
history = stock.history(period="5d")
print(history)