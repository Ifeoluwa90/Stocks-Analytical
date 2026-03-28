import math
import yfinance as yf

# Valuation thresholds
PE_UNDERVALUED = 15
PE_OVERVALUED = 25
UPSIDE_STRONG_BUY = 20
WEEK52_BOTTOM = 30
WEEK52_TOP = 70

def safe_to_html(df):
    try:
        return df.to_html()
    except Exception:
        return "<p>Data not available</p>"

def _clean_series(series):
    """Convert a pandas Series to a list, replacing NaN with None for JSON."""
    return [None if math.isnan(x) else round(x, 2) for x in series]

def get_stock(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    # Return None if yfinance gives back an empty/invalid response
    if not info or (info.get("trailingPegRatio") is None and info.get("shortName") is None):
        return None

    historical_data = stock.history(period="1y")
    if historical_data.empty:
        return None

    current_price = (
        info.get("currentPrice") or
        info.get("regularMarketPrice") or
        info.get("navPrice") or
        info.get("previousClose") or
        0
    )
    high = round(historical_data["High"].max(), 2)
    low = round(historical_data["Low"].min(), 2)

    try:
        analyst_data = stock.get_analyst_price_targets()
        mean_target = analyst_data.get("mean") or "N/A"
    except Exception:
        mean_target = "N/A"

    # Next earnings date
    try:
        calendar = stock.calendar
        ed = calendar.get("Earnings Date")
        if ed is not None and len(ed) > 0:
            earnings_date = str(ed[0].date()) if hasattr(ed[0], "date") else str(ed[0])
        else:
            earnings_date = "N/A"
    except Exception:
        earnings_date = "N/A"

    dates = historical_data.index.strftime("%Y-%m-%d").tolist()
    prices = _clean_series(historical_data["Close"])

    # Rolling moving averages
    ma50  = _clean_series(historical_data["Close"].rolling(50).mean())
    ma200 = _clean_series(historical_data["Close"].rolling(200).mean())

    news_raw = stock.news[:5]
    news = []
    for article in news_raw:
        try:
            news.append({
                "title": article["content"]["title"],
                "link": article["content"]["canonicalUrl"]["url"],
                "publisher": article["content"]["provider"]["displayName"],
                "thumbnail": article["content"]["thumbnail"]["resolutions"][1]["url"]
            })
        except (KeyError, IndexError, TypeError):
            pass

    # Day change
    day_change = round(info.get("regularMarketChange") or 0, 2)
    day_change_pct = round(info.get("regularMarketChangePercent") or 0, 2)

    # Dividend yield stored as a decimal in yfinance (0.015 = 1.5%)
    raw_div = info.get("dividendYield") or 0
    dividend_yield = round(raw_div * 100, 2) if raw_div < 1 else round(raw_div, 2)

    return {
        "name": info.get("shortName", "N/A"),
        "longname": info.get("longName", "N/A"),
        "price": current_price,
        "sector": info.get("sector") or info.get("category", "N/A"),
        "high": high,
        "low": low,
        "pe_ratio": round(info.get("trailingPE") or 0, 2),
        "forward_pe": round(info.get("forwardPE") or 0, 2),
        "eps": info.get("trailingEps") or "N/A",
        "analyst_target": mean_target,
        "market_cap": info.get("marketCap"),
        "dividend_yield": dividend_yield,
        "beta": round(info.get("beta") or 0, 2),
        "day_change": day_change,
        "day_change_pct": day_change_pct,
        "earnings_date": earnings_date,

        # Chart data
        "dates": dates,
        "prices": prices,
        "ma50": ma50,
        "ma200": ma200,

        # Financials
        "news": news,
        "income_stmt": safe_to_html(stock.income_stmt),
        "quarterly_income": safe_to_html(stock.quarterly_income_stmt),
        "balance_sheet": safe_to_html(stock.balance_sheet),
        "cashflow": safe_to_html(stock.cashflow),
    }

def get_stockvaluation(stock_data):
    current_price = stock_data["price"]
    high = stock_data["high"]
    low = stock_data["low"]
    analyst_target = stock_data["analyst_target"]
    P_E = stock_data["pe_ratio"]

    upside_pct = "N/A"
    upside_signal = "No data"
    week52_position = "N/A"
    week52_signal = "No data"

    # Formula 1 — P/E Ratio
    if P_E and P_E != "N/A" and P_E > 0:
        if P_E < PE_UNDERVALUED:
            pe_signal = "Potentially undervalued"
        elif P_E <= PE_OVERVALUED:
            pe_signal = "Fairly valued"
        else:
            pe_signal = "Potentially overvalued"
    else:
        P_E = "N/A"
        pe_signal = "Not enough data"

    # Formula 2 — Upside %
    if analyst_target and analyst_target != "N/A" and current_price:
        upside_pct = ((analyst_target - current_price) / current_price) * 100
        if upside_pct > UPSIDE_STRONG_BUY:
            upside_signal = "Strong Buy signal"
        elif upside_pct >= 0:
            upside_signal = "Hold"
        else:
            upside_signal = "Overvalued vs expectations"

    # Formula 3 — 52 Week Position
    if high != low:
        week52_position = ((current_price - low) / (high - low)) * 100
        if week52_position < WEEK52_BOTTOM:
            week52_signal = "Near bottom, possible opportunity"
        elif week52_position <= WEEK52_TOP:
            week52_signal = "Middle of range"
        else:
            week52_signal = "Near peak, be cautious"

    return {
        "pe_ratio": P_E,
        "pe_signal": pe_signal,
        "upside_pct": round(upside_pct, 2) if upside_pct != "N/A" else "N/A",
        "upside_signal": upside_signal,
        "week52_position": round(week52_position, 2) if week52_position != "N/A" else "N/A",
        "week52_signal": week52_signal
    }
