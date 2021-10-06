--
-- File generated with SQLiteStudio v3.3.2 on sam. mars 27 18:44:49 2021
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Messages
CREATE TABLE Messages (
    MessageId INTEGER PRIMARY KEY,
    Content   TEXT    NOT NULL,
    Author    TEXT    NOT NULL,
    IsSpam    INTEGER,
    Date      TEXT    NOT NULL
);


-- Table: Prediction
CREATE TABLE Prediction (
    PredictionID INTEGER PRIMARY KEY,
    Prediction   REAL NOT NULL,
    Confidence   REAL NOT NULL,
    MessageId    INTEGER NOT NULL,
    FOREIGN KEY (
        MessageId
    )
    REFERENCES Messages (MessageId) 
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
