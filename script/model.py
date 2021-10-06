#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

def trainAndDumpVectorizer(path=None):
    """
    This function is your bread and butter, she will open the dataset you will pass in command line argument or use the default "spam.csv" one
    She will cleanup the data by transforming the class into binary value
    She will train a simple word count model and dump the model and the vectorizer in the current folder
    
    to further train the model you can start coding before line 46 which are the model dumping. 


    

    Args:
        path (str, optional): path to the csv file. Defaults to None.
    
    Returns:
        vectorizer: fitted count Vectorizer
        classifier: trained classifier
    """

    if path == None:
        path = "./Data/spam.csv" #If no arguments are passed we use the default csv
    df = pd.read_csv(path,delimiter=",",error_bad_lines=False,header=None,
    names=["CLASS", "CONTENT"])
    df["CONTENT"] = df["CONTENT"].astype(str)
    df = df.replace({"CLASS": {"spam":1,"not_spam":0}}) # working with binary looks better

    df_train, df_test = train_test_split(df, test_size=0.2, random_state=57)
    y_train = df_train['CLASS'].values
    vectorizer = CountVectorizer() # We tokenize our dataset, so count each time a word or token appeared and return an array
    X_train = vectorizer.fit_transform(list(df_train['CONTENT'].values)).todense()

    classifier = LogisticRegression().fit(X_train,y_train)
    pickle.dump(classifier, open('./models/final_prediction.pickle', 'wb'))
    pickle.dump(vectorizer, open('./models/final_prediction_vectorizer.pickle', 'wb'))
    return vectorizer, classifier

def predict(message):
    """
    basic prediction function.
    train and loads the model before making a prediction and returning the result
    Args:
        message (str): message that you want to test

    Returns:
        int: result of the prediction, 1 if it's a spam 0 otherwise
    """
    vectorizer,classifier = trainAndDumpVectorizer()
    X_test = vectorizer.transform(message).todense()
    predction = classifier.predict(X_test)
    return predction[0]



if __name__ == '__main__':

    """
    Base usage will be : python3 model.py pathToDataSet MessageToCheck
    """
    path = sys.argv[0] # we'll pass the source file as a CLI argument
    # message = sys.argv[1]
    vectorizer,classifier = trainAndDumpVectorizer()
    # print(predict(message))
