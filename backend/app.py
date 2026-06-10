import os
import pymysql
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS so the frontend can interact with this API
CORS(app) 

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER", "myuser"),
        password=os.environ.get("DB_PASSWORD", "mypassword"),
        database=os.environ.get("DB_NAME", "appdb"),
        cursorclass=pymysql.cursors.DictCursor
    )

# Route to get all messages
@app.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Fetch the 10 most recent messages
            cursor.execute("SELECT id, content FROM messages ORDER BY id DESC LIMIT 10;")
            result = cursor.fetchall()
        conn.close()
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Route to add a new message
@app.route('/api/messages', methods=['POST'])
def add_message():
    try:
        data = request.get_json()
        content = data.get('content')
        
        if not content:
            return jsonify({"status": "error", "message": "Message content is required"}), 400
            
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO messages (content) VALUES (%s)", (content,))
        conn.commit() # Save the changes
        conn.close()
        
        return jsonify({"status": "success", "message": "Saved to database!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
