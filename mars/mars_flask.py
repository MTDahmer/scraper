from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import requests


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")


@app.route('/')
def init():
    scrape_data = mongo.db.collection.find_one()

    return render_template("index.html", mars=scrape_data)


@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()

    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

 