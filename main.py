from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():
    return "API شغالة"

@app.route("/notes")
def get_notes():
    db = mysql.connector.connect(
        host="mysql-200014-0.cloudclusters.net",
        port=19100,
        user="root",
        password="nnmm2244",
        database="Mydb"
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(result)
