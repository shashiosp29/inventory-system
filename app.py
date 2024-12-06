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

@app.route('/api/items', methods=['GET'])
def get_items():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return jsonify(items)

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, quantity) VALUES (?, ?)", (name, quantity))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item added'}), 201

if __name__ == '__main__':
    app.run(debug=True)

