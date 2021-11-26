import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.activate import iterateInvestments, singleInvestment

app = Flask(__name__)
CORS(app)

@app.route("/", methods = ["GET"])
def check():
    return "Alive!"

@app.route("/results/", methods = ["POST"])
# drag-and-drop section for excel files
def results_from_df():
    excelFile = "C:/Users/pdewilde/Documents/Projects/AG2R/assets/data.xlsx"
    dfScraped = iterateInvestments(excelFile)
    return dfScraped

# query box for single results
def results_from_input():
    ISIN = input
    result = singleInvestment(ISIN)
    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host = "0.0.0.0", threaded = True, port = port)