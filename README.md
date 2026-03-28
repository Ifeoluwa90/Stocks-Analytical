# StockView Terminal

A personal stock analytics dashboard built with Python and Flask. Search any stock or ETF by ticker symbol and get real-time data, valuation signals, price history charts, latest news, and financial statements, all in one place.

---

## Features

- Live Stock and ETF Data — pulls real-time prices, sector, EPS, and analyst targets via yfinance
- Investor Metrics — market cap, dividend yield, beta, forward P/E, next earnings date, day change
- Valuation Signals — three investor-grade formulas to assess whether a stock is worth buying
- Moving Averages — 50D and 200D MA lines overlaid on the price chart
- 1-Year Price Chart — interactive Chart.js line chart with gradient fill and custom tooltips
- Latest News — top 5 news articles with thumbnails and publisher names
- Financial Statements — toggle between Annual Earnings, Quarterly Earnings, Balance Sheet, and Cash Flow
- ETF Support — handles both stocks and ETFs gracefully (sector vs category fallback)
- Smart Caching — stock data cached for 15 minutes to improve speed and reduce API calls
- Watchlist — save tickers to a persistent watchlist via localStorage, shown on the home page
- Inline Search — search a new ticker directly from the results page

---

## Valuation Formulas

### 1. P/E Ratio (Price-to-Earnings)
Measures whether a stock is priced fairly relative to its earnings.
```
P/E = Current Price / Earnings Per Share

< 15        -> Potentially undervalued
15 - 25     -> Fairly valued
> 25        -> Potentially overvalued
```

### 2. Analyst Upside %
Compares the current price to the mean analyst price target.
```
Upside % = ((Analyst Target - Current Price) / Current Price) x 100

> 20%       -> Strong Buy signal
0% - 20%    -> Hold
Negative    -> Overvalued vs expectations
```

### 3. 52-Week Position
Shows where the current price sits within its yearly range.
```
Position % = ((Current Price - 52W Low) / (52W High - 52W Low)) x 100

< 30%       -> Near bottom, possible opportunity
30% - 70%   -> Middle of range
> 70%       -> Near peak, be cautious
```

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Backend | Python + Flask | Web server and routing |
| Data | yfinance | Real-time stock and ETF data |
| Frontend | HTML + CSS + JS | Dashboard interface |
| Charts | Chart.js | Interactive price history chart |
| Templating | Jinja2 | Passing Python data into HTML |
| Caching | Flask-Caching | 15-minute in-memory cache |
| Server | Gunicorn | Production WSGI server |
| Hosting | PythonAnywhere | Cloud hosting (free tier) |

---

## Project Structure

```
Stocks-Analytical/
|
+-- main/
    +-- app.py                  # Flask routes and app entry point
    +-- stocks.py               # Data fetching and valuation logic
    +-- requirements.txt        # Python dependencies
    +-- wsgi.py                 # PythonAnywhere WSGI config
    |
    +-- templates/
        +-- home.html           # Search page
        +-- results.html        # Dashboard results page
        +-- about.html          # About page
        +-- error.html          # Error page (invalid ticker / API failure)
```

---

## Getting Started (Local)

### 1. Clone the repository
```bash
git clone https://github.com/Ifeoluwa90/Stocks-Analytical.git
cd Stocks-Analytical/main
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

---

## Deployment (PythonAnywhere)

This app is hosted on [PythonAnywhere](https://www.pythonanywhere.com) — free tier, no hardware required.

### Setup

1. Sign up at **pythonanywhere.com**
2. Go to **Dashboard → Web → Add a new web app → Manual configuration → Python 3.10**
3. Open a Bash console and run:

```bash
git clone https://github.com/Ifeoluwa90/Stocks-Analytical.git
cd Stocks-Analytical/main
pip install -r requirements.txt --user
```

4. In the **Web tab → WSGI configuration file**, replace the contents with `wsgi.py` — update `<your-username>` to your PythonAnywhere username
5. Click **Reload** — the app will be live at `<username>.pythonanywhere.com`

### Updating after changes

```bash
cd Stocks-Analytical && git pull
touch /var/www/<username>_pythonanywhere_com_wsgi.py
```

---

## Usage

1. Enter a stock or ETF ticker on the home page (e.g. AAPL, TSLA, SPY) or click a suggestion pill
2. View the live price, day change, and key investor metrics
3. Check valuation signals and the beta risk indicator
4. Scroll down to see the 1-year price chart with 50D and 200D moving averages
5. Read the latest news with thumbnails and source links
6. Toggle Annual Earnings, Quarterly Earnings, Balance Sheet, or Cash Flow
7. Save stocks to your watchlist with the **+ WATCHLIST** button — they appear on the home page

---

## Known Considerations

- ETFs do not have P/E ratio or EPS data — these will show as N/A
- News requires yfinance v0.2.x+ due to updated Yahoo Finance API structure
- Financial statements may be unavailable for some tickers — handled gracefully
- PythonAnywhere free tier has a daily CPU allowance — sufficient for personal/low-traffic use

---

## Data Source

All data is sourced from [yfinance](https://github.com/ranaroussi/yfinance) — a free, open-source Python library that pulls data from Yahoo Finance. No API key required.

Disclaimer: This dashboard is for personal and educational use only. Nothing here constitutes financial advice. Always do your own research before making investment decisions.

---

## Credits

- Built by — Ife
- UI Design — [Claude](https://claude.ai) (Anthropic)
- Data — yfinance / Yahoo Finance
- Charts — Chart.js
- Fonts — Syne + Space Mono (Google Fonts)
- Hosting — PythonAnywhere

---

## What I Learned Building This

This project was built from scratch as a Python learning journey, going from complete beginner to a working full-stack web application deployed to the cloud. Key concepts covered:

- Python fundamentals (variables, loops, conditionals, functions)
- Working with external libraries and APIs
- Flask routing and templating with Jinja2
- DataFrames with pandas via yfinance
- HTML structure and CSS styling
- JavaScript for chart rendering and UI interactions
- Handling real-world data edge cases (missing fields, ETF vs stock differences)
- Input validation and error handling
- Caching strategies for API-heavy applications
- Git version control and branch management
- Cloud deployment with PythonAnywhere

---

*Built with curiosity and a lot of debugging. 🐛*
