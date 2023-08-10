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

@app.route('/hello')
def hello():
    return "Hello World"


@app.route('/data', methods=['GET'])
def get_data():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM items"
            cursor.execute(query)
            data = cursor.fetchall()

            # Convert rows to list of dictionaries
            result = [{'Name': row[0], 'Qty': row[1]} for row in data]

            cursor.close()
            connection.close()

            return jsonify(result)  # jsonify the list of dictionaries
        else:
            return "Unable to connect to the database", 500
    except Exception as e:
        return "An error occurred: " + str(e), 500

@app.route('/data', methods=['PUT'])
def put_data():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            # Extract data from request JSON
            data = request.json
            value1 = data.get('Name')  
            value2 = data.get('Qty')  
            
            query = "INSERT INTO items (Name, Qty) VALUES (?, ?)"
            cursor.execute(query, (value1, value2))
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
