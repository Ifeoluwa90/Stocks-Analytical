import yfinance as yf

def get_stock(ticker):
    stock = yf.Ticker(ticker)
    # Get info
    info = stock.info
    historical_data = stock.history(period="1y")
    return {
        "name": info["shortName"],
        "price": info["currentPrice"],
        "sector": info["sector"],
        "high": round(historical_data["High"].max(), 2),
        "low": round(historical_data["Low"].min(), 2),
    }