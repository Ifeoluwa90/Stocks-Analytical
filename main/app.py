import os
import re
from flask import Flask, render_template, request
import stocks
from flask_caching import Cache

app = Flask(__name__)
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 900  # 15 minutes
cache = Cache(app)

TICKER_RE = re.compile(r'^[A-Z]{1,5}$')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/search", methods=["POST"])
def search():
    ticker = request.form.get("ticker", "").strip().upper()

    if not ticker or not TICKER_RE.match(ticker):
        return render_template("error.html", ticker=ticker,
                               message="Invalid ticker symbol. Use 1–5 letters (e.g. AAPL, SPY).")

    cached = cache.get(ticker)
    if cached:
        return render_template("results.html", data=cached)

    try:
        stock_data = stocks.get_stock(ticker)
        if stock_data is None:
            return render_template("error.html", ticker=ticker,
                                   message="No data found. Check the ticker and try again.")
        valuation_data = stocks.get_stockvaluation(stock_data)
        combined = {**stock_data, **valuation_data}
        cache.set(ticker, combined)
        return render_template("results.html", data=combined)
    except Exception as e:
        return render_template("error.html", ticker=ticker,
                               message="Could not fetch data. The ticker may be invalid or the data source is unavailable.")

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", debug=debug)
