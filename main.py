import os
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/", methods = ["GET"])
def check():
    return "Alive!"

@app.route("/results/", methods = ["POST"])
def results_from_df():

def results_from_input():
    

# Two options:
    # - from dataframe
    # - input of ISIN

if __name__ == "__main__:

