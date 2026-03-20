# Importing req
from flask import Flask, render_template, request
import stocks

app = Flask(__name__)

# Creating Homepage
@app.route("/")
def home():
    return render_template("home.html")

# Creating about page
@app.route("/about")
def about():
    return render_template("about.html")

# adding a route to search
@app.route("/search", methods=["POST"])
def search():
    ticker = request.form["ticker"].upper()
    
    stock_data = stocks.get_stock(ticker)
    valuation_data = stocks.get_stockvaluation(ticker)
    
    combined = {**stock_data, **valuation_data}
    
    return render_template("results.html", data=combined)

if __name__ == "__main__":
    app.run(debug=True)