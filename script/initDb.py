import sqlite3

def initDb(): 
    """[summary]
    This function will read the dump.sql file that should be placed in the sql folder and initialize the database with it.
    The database is composed of 2 tables 
    ----------
    Messages that stores the messages Content and if they are a spam or not
    a Prediction table that will store the result of our prediction with the confidence of the model, this should be useful to check the prediction history and see if we're too close to the 0.5 threshold
    """
    con = sqlite3.connect('./script/database.db')
    f = open('./sql/dump.sql','r')
    str = f.read()
    cur = con.cursor()
    cur.executescript(str)
    print("Database succesfully created and saved")

if __name__ == "__main__":
    initDb()