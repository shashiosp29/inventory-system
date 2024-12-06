from flask import Flask, jsonify, request, send_from_directory, session, redirect, url_for, render_template
import sqlite3
import os
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24) 
DATABASE = 'inventory.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            quantity INTEGER
        )
    ''')
    conn.commit()
    conn.close()
create_table()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = hash_password(password)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            session['username'] = user[1]  
            return redirect(url_for('inventory')) 
        else:
             return render_template('login.html', error="Invalid credentials")

    return render_template('login.html') 


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/inventory') 
def inventory():
    if not session.get('logged_in'): 
        return redirect(url_for('login'))
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        conn.close()
        return render_template('inventory.html', items=items, username = session.get('username'))

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/items', methods=['GET', 'POST'])
def manage_items():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401



@app.route('/api/items/<int:item_id>', methods=['PUT', 'DELETE'])
def manage_item(item_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve(path):
    return send_from_directory('client', path)


if __name__ == '__main__':
    app.run(debug=True)
