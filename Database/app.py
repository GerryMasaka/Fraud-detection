from flask import Flask, jsonify, request
import sqlite3
import threading

app = Flask(__name__)

# Create a database connection
conn = sqlite3.connect('Fraud5.db')

cursor = conn.cursor()
# Create a table for storing data
cursor.execute('''CREATE TABLE IF NOT EXISTS mytable(id INTEGER PRIMARY KEY AUTOINCREMENT,senderAccountNumber STRING NOT NULL,pin STRING NOT NULL, receiverAccountNumber STRING NOT NULL, transactionAmount STRING NOT NULL, token STRING NOT NULL)''')
# API endpoint for adding new data
@app.route('/posts', methods=['POST'])
def add_data():
     if request.method == 'POST':
        # Get the data from the request JSON
        senderAccountNumber = request.json['senderAccountNumber']
        pin = request.json['pin']
        receiverAccountNumber = request.json['receiverAccountNumber']
        transactionAmount = request.json['transactionAmount']
        token=request.json['token']

       # print(amount)

        # Connect to the database
        conn = sqlite3.connect('Fraud5.db')
        cursor = conn.cursor()

        # Execute the INSERT statement
        cursor.execute("INSERT INTO mytable (senderAccountNumber, pin, receiverAccountNumber, transactionAmount, token) VALUES (?, ?, ?, ?, ?)", (senderAccountNumber, pin, receiverAccountNumber, transactionAmount, token))

        # Commit the transaction and close the database connection
        conn.commit()
        conn.close()

        # Return a response to the client
        return 'Data added successfully'
     else:
        return 'Invalid request method'

# API endpoint for retrieving data
@app.route('/fetch', methods=['GET'])
def get_data():
     cursor = conn.execute("SELECT * from mytable")
     data = []
     for row in cursor:
        data.append({'id': row[0], 'amount': row[1], 'userPhone': row[2], 'pin' : row[3]})
     return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)
