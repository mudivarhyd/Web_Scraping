# Import all modules
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

# Create instance of Flask app
app = Flask(__name__)
# setup mongo connection
#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

mars_data = {}

# Create route that renders index.html templates
@app.route("/")
def home():
    mars  = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Route for scrape function
@app.route("/scrape")
def scrape():
    
    # Run scrape function
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
