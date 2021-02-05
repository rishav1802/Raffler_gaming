import sqlite3

from flask import Flask, g, request
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
        winners = g.db.execute("SELECT * FROM Events").fetchall()
        g.db.commit()
        print(winners)
        winners = [winners]
        return winners;



@app.route('/add_user', methods=('GET', 'POST'))
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        print("username is:" + username);
        s=""
        s+=username;
        username = [username];
        g.db.execute("INSERT INTO Users( Name) VALUES(?)", username);
        g.db.commit() 
        s+=" added successfully";
        return s;
        # print(username + "added successfully");

@app.route('/participate', methods=["POST"])
def register_event():
    if request.method == 'POST':
        uid = request.form['userid']
        eid = request.form['eventid']
        # If (uid, eid) already present in Table return error

        # if(g.db.execute("SELECT User_Id, Event_Id FROM Participate WHERE (User_Id = uid and Event_Id = eid")):
        #     str="User cannot participate again in the same event"
        #     print(str)
        #     return str;
        # else:
        pdata = [uid, eid]
        g.db.execute("INSERT INTO Participate(User_Id, Event_Id) VALUES(?, ?)", pdata)
        g.db.commit()
        s="Registered User with ID" +uid +" Successfully for Event ID" +eid  
        return s;

@app.route('/winner', methods = ["POST"])
def event_winner():
    """PIcks random participant as winner for an event"""
    if request.method == 'POST':
        eid = request.form['eventid']
        print(eid)
        users = g.db.execute("SELECT User_Id from PARTICIPATE WHERE Event_Id = eid").fetchall()
        user = random.SystemRandom().choice(users)
        print(user + "winner" + eid)
        g.db.commit()



def build_db():
    # print("building database")
    """Builds the database if necessary"""
    conn = sqlite3.connect('raffle.db')
    cursor = conn.cursor()
    
    # cursor.execute('CREATE TABLE Events (id INTEGER PRIMARY KEY AUTOINCREMENT, Event_Date TEXT PRIMARY KEY, Rewards TEXT )')
    # print(" Events Table Created")

    # cursor.execute('CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT)')
    # print("User Table Created")
    
    # cursor.execute('CREATE TABLE Participate (User_Id INTEGER, Event_Id INTEGER, PRIMARY KEY(User_Id, Event_Id), FOREIGN KEY(User_Id) REFERENCES Users (id), FOREIGN KEY(Event_Id) REFERENCES Events (id))')
    # print("Participate table created")

    # cursor.execute('CREATE TABLE Winner (Event_Id INTEGER, Name TEXT, Rewards TEXT, PRIMARY KEY(Event_Id), FOREIGN KEY(NAME) REFERENCES Users (Name), FOREIGN KEY(Rewards) REFERENCES Events (Rewards) )')
    # cursor.execute('CREATE TABLE ')

    # db.execute("""CREATE TABLE Register_event (

    # )""" )

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
    build_db()
    app.run()




