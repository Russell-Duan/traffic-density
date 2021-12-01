from flask import Flask, render_template, request, g

import sqlite3

app = Flask(__name__)

def get_message_db():
    if 'message_db' not in g: # to see if the meesage_db is in the app
        g.message_db = sqlite3.connect("messages_db.sqlite") # connect to this database
    g.message_db = sqlite3.connect("messages_db.sqlite")
    cur = g.message_db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS messages (
    id INT(9) NOT NULL, 
    handle VARCHAR(65535) DEFAULT NULL, 
    message VARCHAR(65535) DEFAULT NULL,
    PRIMARY KEY(id)
    )''') # execute the SQL command
    g.message_db.commit() # save the changes
    g.message_db.close()
    
    return g.message_db

def insert_message(request):
    if request.method == 'POST':
        message = request.form['message']
        handle = request.form['handle']
    g.message_db = sqlite3.connect("messages_db.sqlite")
    cur = g.message_db.cursor()
    cur.execute('''SELECT count() FROM messages''')
    ID = cur.fetchall()[0][0]
    cur.execute('INSERT INTO messages (ID, handle, message) VALUES (?, ?, ?)',
                (ID, handle, message)
            )
    g.message_db.commit()
    g.message_db.close()

    return g.message_db

def random_messages(n):
    g.message_db = sqlite3.connect("messages_db.sqlite")
    cur = g.message_db.cursor()
    cur.execute('SELECT * FROM messages ORDER BY RANDOM() LIMIT '+ str(n))
    res = cur.fetchall()
    return res

@app.route("/")

def main():
    return render_template("main.html")

# getting basic user data
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        g.message_db = get_message_db()
        insert_message(request)
    return render_template("submit.html")

@app.route('/view/', methods=['POST', 'GET'])
def view():
    res = random_messages(3)
    return render_template("view.html", res = res)