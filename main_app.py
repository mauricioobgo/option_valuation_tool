from flask import Flask,render_template, url_for, request, redirect,jsonify
from class_valuation_calculus import valuation_calculus as valuation
from datetime import datetime
import logging
import os
logging.basicConfig(level=logging.DEBUG)

#Init app
#falta terminación app
app=Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))

#Initialize Module of Valuation
new_valuation_type=valuation()

array_type_option=['Call Europea','Put Europea','Call Americana','Put Americana']
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")

@app.route('/process')
def process():
    return jsonify(option_type= "Response_ok")

if __name__=="__main__":
    app.run(debug=True)