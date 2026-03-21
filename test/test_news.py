import yfinance as yf

stock = yf.Ticker("AAPL")
news_raw = stock.news

print(news_raw[0])