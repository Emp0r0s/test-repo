from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

# Get the Azure SQL Database connection string from environment variables
connection_string = os.environ.get('SQLCONNSTR_mydbconnection')

# Function to establish a database connection
def get_db_connection():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None
#123
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM items"
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(data)
        else:
            return "Unable to connect to the database", 500
    except Exception as e:
        return "An error occurred: " + str(e), 500

@app.route('/put_data', methods=['PUT'])
def put_data():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            # Extract data from request JSON
            data = request.json
            query = "INSERT INTO items (column1, column2) VALUES (?, ?)"
            cursor.execute(query, data['value1'], data['value2'])
            connection.commit()
            cursor.close()
            connection.close()
            return "Data inserted successfully"
        else:
            return "Unable to connect to the database", 500
    except Exception as e:
        return "An error occurred: " + str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
