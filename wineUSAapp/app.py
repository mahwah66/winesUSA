from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import json
import scraper

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/wines")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    winfo =  mongo.db.winesall.find().sort([("dt_published", -1)])
    #print(winfo)
    if winfo==None:
        print('hi')
        #return redirect("/scrape")
    else:
        wlist=[]
        for rec in winfo:
            try:
                del rec["_id"]
            except KeyError:
                print("Key '_id' not found")
            wlist.append(rec)
        return render_template("index.html", winfo = wlist)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    print('scrape')
    scraper.scrapeNew()
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
