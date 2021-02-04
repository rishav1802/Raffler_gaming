import sqlite3

from flask import Flask, g

app = Flask(__name__)

DATABASE = 'database.db'

@app.before_request
def before_request():
    """Connects to the database on each request"""
    g.db = sqlite3.connect(DATABASE)

@app.after_request
def after_request(response):
    """Close the db connection"""
    g.db.close()
    return response

def build_db():
    # print("building database")
    """Builds the database if necessary"""
    db = sqlite3.connect('raffle.db')
    # db = dbi.cursor()
    # try:
    #     db.execute('SELECT 1 FROM Events')
    #     # print(db.fetchone())
    # except sqlite3.OperationalError:
    #     with db:
    # db.execute('CREATE TABLE Events (id INTEGER PRIMARY KEY, Event_Date TEXT, Rewards TEXT )')

    # db.execute('CREATE TABLE Users (id INTEGER PRIMARY KEY, Name TEXT, Ticket TEXT )')
    # db.execute("""CREATE TABLE Register_event (

    # )""" )
    # db.execute("""CREATE TABLE winner (
    #         participant_id INTEGER,
    #         prize_name TEXT,
    #         FOREIGN KEY(participant_id) REFERENCES participants(id)
    #     )""")

    with open('data.txt', 'r') as data:
        # users = set()
        for line in data.readlines():
            event, reward = (line.strip().split(","))
            print(event + reward) 
            db.execute("INSERT INTO Events(Event_Date, Rewards) VALUES", (event, reward))
            
        # for user in users:
        #     db.execute("""INSERT INTO Events(name)
        #         VALUES (?)""", (user,))

    db.close()

if __name__ == '__main__':
    build_db()
    app.run()



# conn = sqlite3.connect('database.db')
# print ("Opened database successfully");

# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print ("Table created successfully");
# conn.close()
