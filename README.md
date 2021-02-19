# Raffler_gaming
Schema:

CREATE TABLE r.Events (eventid INTEGER PRIMARY KEY AUTOINCREMENT, eventdate TEXT, rewards TEXT );

CREATE TABLE r.Users (ticketid INTEGER PRIMARY KEY, name TEXT);

CREATE TABLE r.TICKETS (ticketid INTEGER PRIMARY KEY, used boolean, FOREIGN KEY(ticketid) REFERENCES USERS (ticketid));

CREATE TABLE r.Participate (userid INTEGER, eventid INTEGER, PRIMARY KEY(userid, eventid));

CREATE TABLE r.Winner (EventDate TEXT, Name TEXT, Rewards TEXT, PRIMARY KEY(EventDate), FOREIGN KEY(NAME) REFERENCES Users (Name), FOREIGN KEY(Rewards) REFERENCES Events (Rewards) );


STEPS:
	open terminal 
	
1. virtualenv env
2. source env/bin/activate
3. pip3 install -r requirements.txt
4. export FLASK_APP = raffler.py
5. flask run

To view contents of a table:
	open terminal
	
1. install sqlite3
2. sqlite3
3. ATTACH 'raffle.db' as r;
4. .tables
5. SELECT * FROM 'TABLE_NAME';
6. .schema

