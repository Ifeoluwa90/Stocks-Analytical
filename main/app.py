from flask import Flask, render_template, request
import stocks

app = Flask(__name__)

# Skip Ngrok browser warning
@app.after_request
def add_ngrok_header(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/search", methods=["POST"])
def search():
    ticker = request.form["ticker"].upper()
    stock_data = stocks.get_stock(ticker)
    valuation_data = stocks.get_stockvaluation(stock_data)
    combined = {**stock_data, **valuation_data}
    return render_template("results.html", data=combined)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)