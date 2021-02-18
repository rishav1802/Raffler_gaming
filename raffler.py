import sqlite3
import random
from flask import Flask, g, request, render_template
app = Flask(__name__)

DATABASE = 'raffle.db'

# eid = "1"

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
def show_next_event():
    """Shows the next lucky draw event timing & corresponding reward"""
    if request.method == 'GET':
        winners = g.cursor.execute("SELECT * FROM Events where eventid =?", eid)
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

        ticketid = request.form['ticketid']
       
        # exists = g.cursor.execute("SELECT * FROM Users where Name = ?", (username,)).fetchall()
        # if exists:
        #     return "User Already Registered"
        # else:
        g.cursor.execute("INSERT INTO Users(ticketid, name) VALUES(?, ?)", (ticketid, username,));
        g.cursor.execute("INSERT INTO Tickets(ticketid, used) VALUES(?, ?)", (ticketid, "false",));
        g.db.commit() 

        users = g.cursor.execute("SELECT * FROM Tickets").fetchall()
        print(users)
        #s=""
        #s+=" added successfully and token no. is:" 
        return render_template('users.html', rows = users);
        # print(username + "added successfully");

# @app.route('show_users')
# def show_user():
#     r = g.cursor.execute("SELECT * FROM Participate Where Event_id=?", eid).fetchall();
#     return render_template('users.html', rows = r)
# @app.route('/show_participants', methods = ["GET"])
# def show_participants():
#     """Shows registered users for the next event"""
    


@app.route('/participate', methods=["POST"])
def register_event():
    '''Registers a user using his token number for the next event'''
    if request.method == 'POST':
        uid = request.form['userid']
        # eid = request.form['eventid']
        # If (uid, eid) already present in Table return error
        
        # exists = g.cursor.execute("SELECT * FROM Users where ticketid = ?", (uid,)).fetchall()
        # if not exists:
        # 	return "Invalid ticket"
        isused = g.cursor.execute("SELECT used FROM TICKETS where ticketid = ?", (uid,)).fetchall()
        
        if (isused[0][0]=="true"):
            return "ticket already used"
        # print(uid +"+"+ eid)


        # evexist = g.cursor.execute("SELECT EVENT_DATE FROM Events where id = ?", (eid,)).fetchall()
        # print(evexist)
        # if not evexist:
        # 	return "Invalid Event id"
        # for eve in evexist[0]:
        # 	ev = eve
        # ev = str(ev)
        # if evexist:
        # 	eventover = g.cursor.execute("SELECT * FROM WINNER WHERE winner.event_date = ?", (ev,)).fetchall()
        # 	if eventover:
        # 		return "Event already Over"
        	
        	
        
        

        # if(g.db.execute("SELECT User_Id, Event_Id FROM Participate WHERE (User_Id = uid and Event_Id = eid")):
        #     str="User cannot participate again in the same event"
        #     print(str)
        #     return str;
        # else:
        # g.cursor.execute("DELETE FROM TICKETS WHERE token =? ", uid)
        g.cursor.execute("UPDATE TICKETS SET used = ? WHERE ticketid = ?",("true", uid,))

        pdata = [uid, eid]
        g.cursor.execute("INSERT INTO Participate(userid, eventid) VALUES(?, ?)", pdata)
        g.db.commit()


        s="Registered User with ID" +uid +" Successfully for Event ID" +eid  
        print(s);
        return s;

@app.route('/show_participants', methods = ["GET"])
def show_participants():
    """Shows registered users for the next event"""
    r = g.cursor.execute("SELECT * FROM Participate Where eventid=?", eid).fetchall();
    return render_template('participate.html', rows = r)


@app.route('/start_lucky_draw', methods = ["GET"])
def event_winner():
    """PIcks random participant as winner for an event"""
    # if request.method == 'POST':
    #     eid = request.form['eventid']
    # print(eid)
    # eventids = g.cursor.execute("SELECT id from EVENTS where id = ? ", (eid,)).fetchall();
    # print(eventids)
    # for eid in eventids:
    # /// SELCT USER IDS FOR THE NEXT EVENT
    usersid = g.cursor.execute("SELECT userid from Participate WHERE eventid = ? ", (eid,)).fetchall()

    userid = random.SystemRandom().choice(usersid)
    print("userid")
    # print(userid)
    # print(userid)
    for id in userid:
        wid = id
    wid = str(wid)
    print(wid)
    edate = g.db.execute("SELECT eventdate FROM EVENTS WHERE eventid = ?", (eid,)).fetchall()
    print(edate)
    for e in edate[0]:
        ed = e
    ed = str(ed)
    reward = g.db.execute("SELECT rewards FROM EVENTS WHERE eventid = ?", (eid,)).fetchall()
    for r in reward[0]:
        re = r
    re = str(re)
    wname = g.db.execute("SELECT name FROM Users WHERE ticketid = ?", (wid,)).fetchall()
    for w in wname[0]:
        wn = w
    wn = str(wn)
    print(type(wn))
    print(wn)
    data = [ed, wn, re]
    g.cursor.execute("INSERT INTO WINNER(eventdate, name, rewards) VALUES(?, ?, ?)", data)

    print(wid)
    s = str(wid) + "is the winner for event" + eid 
    print(s)
    g.db.commit()
    modify_event()
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
    
    # cursor.execute('CREATE TABLE Events (eventid INTEGER PRIMARY KEY AUTOINCREMENT, eventdate TEXT, rewards TEXT )')
    # print(" Events Table Created")

    # cursor.execute('CREATE TABLE Users (ticketid INTEGER PRIMARY KEY, name TEXT)')
    # print("User Table Created")

    # cursor.execute('CREATE TABLE TICKETS (ticketid INTEGER PRIMARY KEY, used boolean, FOREIGN KEY(ticketid) REFERENCES USERS (ticketid))')
    # print("TICKET Table Created")
    
    # cursor.execute('CREATE TABLE Participate (userid INTEGER, eventid INTEGER, PRIMARY KEY(userid, eventid))')
    # print("Participate table created")

    # cursor.execute('CREATE TABLE Winner (eventdate TEXT, name TEXT, rewards TEXT, PRIMARY KEY(eventdate), FOREIGN KEY(name) REFERENCES Users (name), FOREIGN KEY(rewards) REFERENCES Events (rewards) )')
    # # print("Winner table created")



    '''Read Information about the Lucky Draw Events from txt file in same folder'''
    
    with open('data.txt', 'r') as data:
        for line in data.readlines():
            event, reward = (line.strip().split(","))
            # print ( event + reward)   
            data = [event, reward]
            try:
                cursor.execute("INSERT INTO Events( eventdate, rewards) VALUES(?, ?)", data)
                conn.commit()
            except Error as err:
                print(err)

    cursor.close()
    conn.close()

def modify_event():
    global eid
    eid = str(int(eid)+1)


if __name__ == '__main__':
    '''run build_db once initially for creating tables'''
    global eid
    eid = "1"
    build_db()
    app.run()




