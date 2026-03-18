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
    ticker = request.form["ticker"] 
    data = stocks.get_stock(ticker)
    return render_template("results.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)