import yfinance as yf

def get_stock(ticker):
    stock = yf.Ticker(ticker)
    
    # Get info
    info = stock.info
    historical_data = stock.history(period="1y")
    current_price = info.get("currentPrice", 0)
    high = round(historical_data["High"].max(), 2)
    low = round(historical_data["Low"].min(), 2)
    analyst_data = stock.get_analyst_price_targets()
    mean_target = analyst_data.get("mean", "N/A")
    
    # For Chart.js - dates and prices
    history = stock.history(period="1y")
    dates = history.index.strftime("%Y-%m-%d").tolist()
    prices = round(history["Close"], 2).tolist()

    return {
        "name": info.get("shortName", "N/A"),
        "longname": info.get("longName", "N/A"),
        "price": current_price,
        "sector": info.get("sector") or info.get("category", "N/A"),
        "high": high,
        "low": low,
        "pe_ratio": round(info.get("trailingPE", 0), 2),
        "eps": info.get("trailingEps", "N/A"),
        "analyst_target": mean_target,
        # For Chart.js - dates and prices
        "dates" : dates,
        "prices" : prices,
    }

def get_stockvaluation(ticker):
    stock_data = get_stock(ticker)

    current_price = stock_data["price"]
    high = stock_data["high"]
    low = stock_data["low"]
    analyst_target = stock_data["analyst_target"]
    P_E = stock_data["pe_ratio"]

    # Defaults — prevents crashes if data is missing
    upside_pct = "N/A"
    upside_signal = "No data"
    week52_position = "N/A"
    week52_signal = "No data"

    # Formula 1 — P/E Ratio
    if P_E and P_E != "N/A" and P_E > 0:
        if P_E < 15:
            pe_signal = "Potentially undervalued 🟢"
        elif P_E <= 25:
            pe_signal = "Fairly valued 🟡"
        else:
            pe_signal = "Potentially overvalued 🔴"
    else:
        P_E = "N/A"
        pe_signal = "Not enough data"

    # Formula 2 — Upside %
    if analyst_target != "N/A":
        upside_pct = ((analyst_target - current_price) / current_price) * 100
        if upside_pct > 20:
            upside_signal = "Strong Buy signal 🟢"
        elif 0 <= upside_pct <= 20:  # ✅ fixed
            upside_signal = "Hold 🟡"
        else:
            upside_signal = "Overvalued vs expectations 🔴"

    # Formula 3 — 52 Week Position
    if high != low:
        week52_position = ((current_price - low) / (high - low)) * 100
        if 0 <= week52_position < 30:
            week52_signal = "Near bottom, possible opportunity 🟢"
        elif 30 <= week52_position <= 70:
            week52_signal = "Middle of range 🟡"
        else:
            week52_signal = "Near peak, be cautious 🔴"

    return {
        "pe_ratio": P_E,
        "pe_signal": pe_signal,
        "upside_pct": round(upside_pct, 2) if upside_pct != "N/A" else "N/A",
        "upside_signal": upside_signal,
        "week52_position": round(week52_position, 2) if week52_position != "N/A" else "N/A",
        "week52_signal": week52_signal
    }