# StockView Terminal
 
A personal stock analytics dashboard built with Python and Flask. Search any stock or ETF by ticker symbol and get real-time data, valuation signals, price history charts, latest news, and financial statements - all in one place.
 
---
 
## Features
 
- **Live Stock & ETF Data** - pulls real-time prices, sector, EPS, and analyst targets via yfinance
- **Valuation Signals** - three investor-grade formulas to assess whether a stock is worth buying
- **1-Year Price Chart** - interactive Chart.js line chart with gradient fill and custom tooltips
- **Latest News** - top 5 news articles relevant to the searched ticker
- **Financial Statements** - toggle between Annual Earnings, Quarterly Earnings, and Balance Sheet
- **ETF Support** - handles both stocks and ETFs gracefully (sector vs category fallback)
 
---
 
## Valuation Formulas
 
### 1. P/E Ratio (Price-to-Earnings)
Measures whether a stock is priced fairly relative to its earnings.
```
P/E = Current Price / Earnings Per Share
 
< 15        → Potentially undervalued 🟢
15 – 25     → Fairly valued 🟡
> 25        → Potentially overvalued 🔴
```
 
### 2. Analyst Upside %
Compares the current price to the mean analyst price target.
```
Upside % = ((Analyst Target - Current Price) / Current Price) × 100
 
> 20%       → Strong Buy signal 🟢
0% – 20%   → Hold 🟡
Negative    → Overvalued vs expectations 🔴
```
 
### 3. 52-Week Position
Shows where the current price sits within its yearly range.
```
Position % = ((Current Price - 52W Low) / (52W High - 52W Low)) × 100
 
< 30%       → Near bottom, possible opportunity 🟢
30% – 70%  → Middle of range 🟡
> 70%       → Near peak, be cautious 🔴
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
 
---
 
## Project Structure
 
```
stockview/
│
├── app.py                  # Flask routes and app entry point
├── stocks.py               # Data fetching and valuation logic
│
└── templates/
    ├── home.html           # Search page
    ├── results.html        # Dashboard results page
    └── about.html          # About page
```
 
---
 
## Getting Started
 
### 1. Clone the repository
```bash
git clone https://github.com/yourusername/stockview.git
cd stockview
```
 
### 2. Install dependencies
```bash
pip install flask yfinance
```
 
### 3. Run the app
```bash
python app.py
```
 
### 4. Open in browser
```
http://127.0.0.1:5000
```
 
---
 
## Usage
 
1. Enter a stock ticker on the home page (e.g. `AAPL`, `TSLA`, `SPY`)
2. View the live price, key stats, and valuation signals
3. Scroll down to see the 1-year price chart
4. Read the latest news affecting the stock
5. Toggle Annual Earnings, Quarterly Earnings, or Balance Sheet as needed
 
---
 
## Data Source
 
All data is sourced from **[yfinance](https://github.com/ranaroussi/yfinance)** - a free, open-source Python library that pulls data from Yahoo Finance. No API key required.
 
> **Disclaimer:** This dashboard is for personal and educational use only. Nothing here constitutes financial advice. Always do your own research before making investment decisions.
 
---
 
## Credits
 
- **Built by** - Ife
- **UI Design** - [Claude](https://claude.ai) (Anthropic)
- **Data** - yfinance / Yahoo Finance
- **Charts** - Chart.js
- **Fonts** - Syne + Space Mono (Google Fonts)
 
---
 
## What I Learned Building This
 
This project was built from scratch as a Python learning journey, going from complete beginner to a working full-stack web application. Key concepts covered:
 
- Python fundamentals (variables, loops, conditionals, functions)
- Working with external libraries and APIs
- Flask routing and templating with Jinja2
- DataFrames with pandas via yfinance
- HTML structure and CSS styling
- JavaScript for chart rendering and UI interactions
- Handling real-world data edge cases (missing fields, ETF vs stock differences)
 
---
 
*Built with curiosity and a lot of debugging. 🐛*
