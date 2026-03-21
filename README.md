# StockView Terminal

A personal stock analytics dashboard built with Python and Flask. Search any stock or ETF by ticker symbol and get real-time data, valuation signals, price history charts, latest news, and financial statements, all in one place.

---

## Features

- Live Stock and ETF Data - pulls real-time prices, sector, EPS, and analyst targets via yfinance
- Valuation Signals - three investor-grade formulas to assess whether a stock is worth buying
- 1-Year Price Chart - interactive Chart.js line chart with gradient fill and custom tooltips
- Latest News - top 5 news articles with thumbnails and publisher names
- Financial Statements - toggle between Annual Earnings, Quarterly Earnings, and Balance Sheet
- ETF Support - handles both stocks and ETFs gracefully (sector vs category fallback)
- Smart Caching - stock data cached for 15 minutes to improve speed and reduce API calls

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
| Server | Gunicorn | Production WSGI server |
| Tunnel | Tunnelmole | Public URL for self-hosted server |
| Hardware | Raspberry Pi 3 A+ | Self-hosted server |

---

## Project Structure

```
Stocks-Analytical/
|
+-- main/
    +-- app.py                  # Flask routes and app entry point
    +-- stocks.py               # Data fetching and valuation logic
    +-- requirements.txt        # Python dependencies
    +-- cache/                  # Cached stock data (auto-generated)
    |
    +-- templates/
        +-- home.html           # Search page
        +-- results.html        # Dashboard results page
        +-- about.html          # About page
```

---

## Getting Started (Local)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/Stocks-Analytical.git
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

## Deployment (Raspberry Pi + Tunnelmole)

This app is self-hosted on a Raspberry Pi running Raspberry Pi OS Lite (64-bit) and exposed to the internet via Tunnelmole.

### Server Setup

```bash
# SSH into the Pi
ssh YOUR_USERNAME@YOUR_PI_IP

# Update and install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git nodejs npm -y

# Clone the project
git clone https://github.com/YOUR_GITHUB_USERNAME/Stocks-Analytical.git
cd Stocks-Analytical/main

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir cache

# Install Tunnelmole
sudo npm install -g tunnelmole
```

### Auto-start with Systemd

Both Gunicorn and Tunnelmole are configured to start automatically on boot.

#### Gunicorn service
Create `/etc/systemd/system/stockview.service`:
```ini
[Unit]
Description=StockView Flask App
After=network.target

[Service]
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/Stocks-Analytical/main
ExecStart=/home/YOUR_USERNAME/Stocks-Analytical/main/venv/bin/gunicorn -w 2 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Tunnelmole service
Create `/etc/systemd/system/tunnelmole.service`:
```ini
[Unit]
Description=Tunnelmole Tunnel
After=network.target stockview.service

[Service]
User=YOUR_USERNAME
ExecStart=/usr/local/bin/tmole 5000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

#### Enable both services
```bash
sudo systemctl enable stockview
sudo systemctl enable tunnelmole
sudo systemctl start stockview
sudo systemctl start tunnelmole
```

#### Verify both are running
```bash
sudo systemctl status stockview
sudo systemctl status tunnelmole
```

### Get the public URL
```bash
curl -s http://localhost:4040/api/tunnels | python3 -m json.tool
```

Share the public URL with friends - no warning page, no sleep, always on.

---

## Usage

1. Enter a stock or ETF ticker on the home page (e.g. AAPL, TSLA, SPY)
2. View the live price, key stats, and valuation signals
3. Scroll down to see the 1-year price chart
4. Read the latest news with thumbnails and source links
5. Toggle Annual Earnings, Quarterly Earnings, or Balance Sheet as needed

---

## Known Considerations

- ETFs do not have P/E ratio or EPS data - these will show as N/A
- News requires yfinance v0.2.x+ due to updated Yahoo Finance API structure
- Financial statements may be unavailable for some tickers - handled gracefully
- Tunnelmole URL changes on restart unless upgraded to a paid plan
- Raspberry Pi 3 A+ has 512MB RAM - avoid more than 2-3 simultaneous users

---

## Data Source

All data is sourced from [yfinance](https://github.com/ranaroussi/yfinance) - a free, open-source Python library that pulls data from Yahoo Finance. No API key required.

Disclaimer: This dashboard is for personal and educational use only. Nothing here constitutes financial advice. Always do your own research before making investment decisions.

---

## Credits

- Built by - Ife
- UI Design - [Claude](https://claude.ai) (Anthropic)
- Data - yfinance / Yahoo Finance
- Charts - Chart.js
- Fonts - Syne + Space Mono (Google Fonts)
- Hosting - Raspberry Pi (self-hosted)
- Tunnel - Tunnelmole

---

## What I Learned Building This

This project was built from scratch as a Python learning journey, going from complete beginner to a working full-stack web application deployed on a real self-hosted server. Key concepts covered:

- Python fundamentals (variables, loops, conditionals, functions)
- Working with external libraries and APIs
- Flask routing and templating with Jinja2
- DataFrames with pandas via yfinance
- HTML structure and CSS styling
- JavaScript for chart rendering and UI interactions
- Handling real-world data edge cases (missing fields, ETF vs stock differences)
- Git version control and branch management
- Linux server administration (SSH, systemd)
- Self-hosted deployment on Raspberry Pi
- Virtual environments and production-grade servers with Gunicorn
- Public tunneling with Tunnelmole

---

*Built with curiosity and a lot of debugging. 🐛*