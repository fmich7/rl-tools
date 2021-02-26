#!/usr/bin/env python
from flask import Flask, render_template, redirect, request
from main import returnListedPricesToServer, returnInOrderedPricesToServer, savePricesToDatabase
import json

app = Flask(__name__)

priceCell_colors = dict()

@app.route("/list")
def list_view():
    priceReduction = request.args.get('lwr', default=100, type=int)
    return render_template("list_view.html", prices=returnListedPricesToServer(priceReduction), colors=priceCell_colors)

@app.route("/ordered")
def offers_view():
    priceReduction = request.args.get('lwr', default=100, type=int)
    return render_template("offers_view.html", prices=returnInOrderedPricesToServer(priceReduction), colors=priceCell_colors)

@app.route("/")
def index():
    return redirect('/list')


@app.route('/save')
def save():
    savePricesToDatabase()
    return "asd"

def loadSettingsFromConfig():
    with open("config.json", 'r') as file:
        data = json.load(file)
        global priceCell_colors
        priceCell_colors = data['settings']['priceCell_colors']

if __name__ == "__main__":
    loadSettingsFromConfig()
    app.run(debug=True)
