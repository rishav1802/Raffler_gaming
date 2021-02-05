# Raffler_gaming
Schema:

CREATE TABLE raffle.Events (id INTEGER PRIMARY KEY AUTOINCREMENT, Event_Date TEXT, Rewards TEXT );


CREATE TABLE raffle.Users (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT);

CREATE TABLE raffle.Participate (User_Id INTEGER, Event_Id INTEGER, PRIMARY KEY(User_Id, Event_Id), FOREIGN KEY(User_Id) REFERENCES Users (id), FOREIGN KEY(Event_Id) REFERENCES Events (id));


CREATE TABLE raffle.Winner (Event_Id INTEGER, Name TEXT, Rewards TEXT, PRIMARY KEY(Event_Id), FOREIGN KEY(NAME) REFERENCES Users (Name), FOREIGN KEY(Rewards) REFERENCES Events (Rewards) );





