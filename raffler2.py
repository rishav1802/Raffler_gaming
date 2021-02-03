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



conn = sqlite3.connect('database.db')
print ("Opened database successfully");

conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print ("Table created successfully");
conn.close()