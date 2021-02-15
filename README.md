# Raffler_gaming
Schema:

CREATE TABLE r.Events (id INTEGER PRIMARY KEY AUTOINCREMENT, Event_Date TEXT, Rewards TEXT );
CREATE TABLE r.Users (token INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT);
CREATE TABLE r.Participate (User_Id INTEGER, Event_Id INTEGER, PRIMARY KEY(User_Id, Event_Id), FOREIGN KEY(User_Id) REFERENCES Users (id), FOREIGN KEY(Event_Id) REFERENCES Events (id));
CREATE TABLE r.Winner (Event_Date TEXT, Name TEXT, Rewards TEXT, PRIMARY KEY(Event_Date), FOREIGN KEY(NAME) REFERENCES Users (Name), FOREIGN KEY(Rewards) REFERENCES Events (Rewards) );

STEPS:

1. virtualenv env
2. source env/bin/activate
3. pip3 install -r requirements.txt
4. export FLASK_APP = raffler.py
5. flask run
