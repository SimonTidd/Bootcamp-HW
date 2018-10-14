from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_Mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_app")


@app.route("/")
def index():
    Mars_data = mongo.db.Mars_data.find_one()
    return render_template("index.html", listings=Mars_data)


@app.route("/scrape")
def scraper():
    Mars_data = mongo.db.listings
    Mars_data_data = scrape_Mars.scrape()
    Mars_data.update({}, Mars_data_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
