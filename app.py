from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = 'inventory.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, quantity INTEGER)''')
    conn.commit()
    conn.close()

create_table()
