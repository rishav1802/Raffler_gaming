import sqlite3
import random
from flask import Flask, g, request, render_template
app = Flask(__name__)

DATABASE = 'raffle.db'

@app.before_request
def before_request():
    """Connects to the database on each request"""
    g.db = sqlite3.connect(DATABASE)
    g.cursor = g.db.cursor()

@app.after_request
def after_request(response):
    """Close the db connection"""
    g.cursor.close()
    g.db.close()
    return response

@app.route('/')
def show_events():
    """Shows the next lucky draw event timing & corresponding reward"""
    if request.method == 'GET':
        winners = g.cursor.execute("SELECT * FROM Events")
        # g.db.commit()
        
        rows = winners.fetchall();
        print(rows)
        # winners = [winners]
        return render_template('events.html', rows = rows )



@app.route('/add_user', methods=['POST'])
def add_user():
    '''Adds a User and assigns him a token number'''
    if request.method == 'POST':
        username = request.form['username']
        print("username is:" + username);
       
        exists = g.cursor.execute("SELECT * FROM Users where Name = ?", (username,)).fetchall()
        if exists:
            return "User Already Registered"
        else:
            g.cursor.execute("INSERT INTO Users( Name) VALUES(?)", (username,));
            g.db.commit() 

            users = g.cursor.execute("SELECT * FROM Users").fetchall()
            print(users)
            #s=""
            #s+=" added successfully and token no. is:" 
            return render_template('users.html', rows = users);
        # print(username + "added successfully");

@app.route('/participate', methods=["POST"])
def register_event():
    '''Registers a user using his token number for a particular event'''
    if request.method == 'POST':
        uid = request.form['userid']
        eid = request.form['eventid']
        # If (uid, eid) already present in Table return error
        
        exists = g.cursor.execute("SELECT * FROM Users where token = ?", (uid,)).fetchall()
        if not exists:
        	return "User not assigned a token yet"
        evexist = g.cursor.execute("SELECT EVENT_DATE FROM Events where id = ?", (eid,)).fetchall()
        print(evexist)
        for eve in evexist[0]:
        	ev = eve
        ev = str(ev)
        if evexist:
        	eventover = g.cursor.execute("SELECT * FROM WINNER WHERE winner.event_date = ?", (ev,)).fetchall()
        	if eventover:
        		return "Event already Over"
        if not evexist:
        	return "Invalid Event id"	
        	
        
        

        # if(g.db.execute("SELECT User_Id, Event_Id FROM Participate WHERE (User_Id = uid and Event_Id = eid")):
        #     str="User cannot participate again in the same event"
        #     print(str)
        #     return str;
        # else:
        pdata = [uid, eid]
        g.cursor.execute("INSERT INTO Participate(User_Id, Event_Id) VALUES(?, ?)", pdata)
        g.db.commit()

        r = g.cursor.execute("SELECT * FROM Participate").fetchall();

        s="Registered User with ID" +uid +" Successfully for Event ID" +eid  
        print(s);
        return render_template('participate.html', rows = r)

@app.route('/start_lucky_draw', methods = ["POST"])
def event_winner():
    """PIcks random participant as winner for an event"""
    if request.method == 'POST':
        eid = request.form['eventid']
        # print(eid)
        # eventids = g.cursor.execute("SELECT id from EVENTS where id = ? ", (eid,)).fetchall();
        # print(eventids)
        # for eid in eventids:
        usersid = g.cursor.execute("SELECT User_Id from Participate WHERE Event_Id = ? ", (eid,)).fetchall()
        userid = random.SystemRandom().choice(usersid)
        print("userid")
        # print(userid)
        # print(userid)
        for id in userid:
            wid = id
        wid = str(wid)
        print(wid)
        edate = g.db.execute("SELECT Event_Date FROM EVENTS WHERE id = ?", (eid,)).fetchall()
        print(edate)
        for e in edate[0]:
            ed = e
        ed = str(ed)
        reward = g.db.execute("SELECT REWARDS FROM EVENTS WHERE id = ?", (eid,)).fetchall()
        for r in reward[0]:
            re = r
        re = str(re)
        wname = g.db.execute("SELECT Name FROM Users WHERE token = ?", (wid,)).fetchall()
        for w in wname[0]:
            wn = w
        wn = str(wn)
        print(type(wn))
        print(wn)
        data = [ed, wn, re]
        g.cursor.execute("INSERT INTO WINNER(Event_Date, Name, Rewards) VALUES(?, ?, ?)", data)

        print(wid)
        s = str(wid) + "is the winner for event" + eid 
        print(s)
        g.db.commit()
        return s

@app.route('/show_winners', methods = ["GET"])
def show_winners():
    '''Shows the winners table'''
    c = g.db.execute('SELECT * FROM WINNER')
    return render_template('winner.html', rows = c.fetchall())



def build_db():
    # print("building database")
    """Builds the database if necessary"""
    conn = sqlite3.connect('raffle.db')
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE Events (id INTEGER PRIMARY KEY AUTOINCREMENT, Event_Date TEXT, Rewards TEXT )')
    print(" Events Table Created")

    cursor.execute('CREATE TABLE Users (token INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT)')
    print("User Table Created")
    
    cursor.execute('CREATE TABLE Participate (User_Id INTEGER, Event_Id INTEGER, PRIMARY KEY(User_Id, Event_Id), FOREIGN KEY(User_Id) REFERENCES Users (id), FOREIGN KEY(Event_Id) REFERENCES Events (id))')
    print("Participate table created")

    cursor.execute('CREATE TABLE Winner (Event_Date TEXT, Name TEXT, Rewards TEXT, PRIMARY KEY(Event_Date), FOREIGN KEY(NAME) REFERENCES Users (Name), FOREIGN KEY(Rewards) REFERENCES Events (Rewards) )')
    print("Winner table created")



    '''Read Information about the Lucky Draw Events from txt file in same folder'''
    
    with open('data.txt', 'r') as data:
        for line in data.readlines():
            event, reward = (line.strip().split(","))
            # print ( event + reward)   
            data = [event, reward]
            try:
                cursor.execute("INSERT INTO Events( Event_Date, Rewards) VALUES(?, ?)", data)
                conn.commit()
            except Error as err:
                print(err)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    '''run build_db once initially for creating tables'''
    #build_db()
    app.run()




