#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 19:24:00 2021

@author: ybettayeb
"""
# never used flask so i'll most likely copy a get started tutorial about it
import flask
from flask import Flask, render_template, url_for, request
from flask import request, jsonify
import pandas as pd
import pickle
import sqlite3 
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
app = Flask(__name__)
app.config["DEBUG"] = True




def dict_factory(cursor, row): 
    """
    wrapper function to turn sqlite rows into dictionnary, to help us jsonify them

    Args:
        cursor (sqliteCursor): connection cursor
        row (cursor.row): sqlQuery Row

    Returns:
        dictionary: dictionnary containing the result of the query
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    """
    basic home page rendering, not much to see there
    """
    return '''<h1>Spam Classifier</h1> <p>prototype API to detect if you're spamming or hamming </p>'''

@app.errorhandler(404)
def page_not_found(e):
    """
    handling of 404 error
    """
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/resources/predictions/all', methods=['GET'])
def api_all():
    """
    this function will return the entire prediction database when queried

    Returns:
        json: query result as a json
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_logs = cur.execute('''SELECT * FROM Prediction INNER JOIN 
        Messages ON Messages.MessageId = Prediction.MessageId 
    WHERE (Prediction.MessageId=Messages.MessageId);''').fetchall()

    return jsonify(all_logs)

@app.route('/api/v1/resources/predictions/spams', methods=['GET'])
def spams():
    """function that will return every message that have been flagged as a spam
    the sql query is simple enough, where we join the messages table with the prediction table and filter with only 1 values that are spams
    Returns:
        [json]: query result as a json
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_logs = cur.execute('SELECT Messages.MessageId as Id, Messages.Content as Message, Prediction.Confidence as Confidence,Messages.Date as Date, Messages.Author as AuthorsIp FROM Messages INNER JOIN Prediction ON Prediction.MessageId = Messages.MessageId WHERE Prediction.Prediction = 1;').fetchall()
    # i should try to make that function propose a download as csv or add another boolean parameter, if parameter == True then we create a csv file with the results named "detectedSpams"+ timestamp
    # so we can then mark them ( Tedious to do manually, need a gui solution but no time to do)
    # and then load the model, fit it on this data and finish the training before redumping it
    return jsonify(all_logs)


@app.route('/api/v1/resources/predictions/predict', methods=['GET'])
def predict():
    
    """bread and butter of the api
    allows you to pass a message and will return the message, the model prediction and it's confidence on the prediction
    this function will load the model and the vectorizer that should be placed in the "models" folder.
    

    Example : api/v1/resources/predictions/predict?Message=Hello do you want to get free money 
    result : {
  "Confidence": 0.5584389870347015, 
  "Message": "Hello do you want to get free money", 
  "Prediction": 0.0
    }
    Returns:
        json: json file with the message, prediction and model's confidence
    """

    loaded_model = pickle.load(open("../models/final_prediction.pickle", 'rb'))
    loaded_vectorizer = pickle.load(open("../models/final_prediction_vectorizer.pickle",'rb'))
    
    params = request.args
    message = params.get('Message')
    data = [message]
    ip_address = flask.request.remote_addr
    vect = loaded_vectorizer.transform(data).todense() 

    my_prediction = float(loaded_model.predict(vect)[0])
    my_confidence = float(max(loaded_model.predict_proba(vect)[0])) # the max value of the array is the probability of the prediction so that's what we want to display 
    # my_confidence = float(loaded_model.predict_proba(vect))
    keys = ['Message','Prediction','Confidence']
    print(my_confidence)
    values = [message,my_prediction, my_confidence]
    date = str(datetime.now()) 
    results = {}
    for i in range(0,len(keys)):
        results[keys[i]] = values[i] # ugly indirection 
        
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        # we want to store our messages and the prediction associated with them, we may also need the confidence of the model in case of false positives that are close to the 0.50 threshold
        # we're also logging the ip of the sender just in case 
        cur.execute("INSERT INTO Messages (Content,Author,IsSpam,Date) VALUES (?,?,?,?)",(data[0],ip_address,my_prediction,date) ) 
        lastRow = cur.lastrowid
        cur.execute("INSERT INTO Prediction (Prediction,Confidence,MessageId) VALUES (?,?,?)",(my_prediction,my_confidence,lastRow) )
        con.commit()
        print("Record successfully added")
        print(results)


    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
