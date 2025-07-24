from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # تفعيل CORS للسماح بطلبات من أي مصدر

# إعدادات قاعدة البيانات
DB_CONFIG = {
    "host": "mysql-200014-0.cloudclusters.net",
    "port": 19100,
    "user": "root",
    "password": "nnmm2244",
    "database": "Mydb"
}

@app.route("/")
def home():
    return "API is running"

@app.route("/notes", methods=['GET'])
def get_notes():
    try:
        # الاتصال بقاعدة البيانات
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor(dictionary=True)

        # جلب جميع الملاحظات
        cursor.execute("SELECT * FROM notes ORDER BY id DESC")
        notes = cursor.fetchall()

        cursor.close()
        db.close()

        return jsonify(notes)

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/notes", methods=['POST'])
def add_note():
    try:
        # الحصول على البيانات من الطلب
        data = request.get_json()
        content = data.get('content')

        if not content:
            return jsonify({"error": "Content is required"}), 400

        # الاتصال بقاعدة البيانات
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        # إضافة ملاحظة جديدة
        cursor.execute("INSERT INTO notes (content) VALUES (%s)", (content,))
        db.commit()

        # الحصول على ID الملاحظة المضافة
        note_id = cursor.lastrowid

        cursor.close()
        db.close()

        return jsonify({
            "id": note_id,
            "content": content,
            "message": "Note added successfully"
        }), 201

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/notes/<int:note_id>", methods=['PUT'])
def update_note(note_id):
    try:
        # الحصول على البيانات من الطلب
        data = request.get_json()
        new_content = data.get('content')

        if not new_content:
            return jsonify({"error": "Content is required"}), 400

        # الاتصال بقاعدة البيانات
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        # تحديث الملاحظة
        cursor.execute("UPDATE notes SET content = %s WHERE id = %s", (new_content, note_id))
        db.commit()

        # التحقق من عدد الصفوف المتأثرة
        if cursor.rowcount == 0:
            return jsonify({"error": "Note not found"}), 404

        cursor.close()
        db.close()

        return jsonify({
            "id": note_id,
            "content": new_content,
            "message": "Note updated successfully"
        })

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/notes/<int:note_id>", methods=['DELETE'])
def delete_note(note_id):
    try:
        # الاتصال بقاعدة البيانات
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        # حذف الملاحظة
        cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        db.commit()

        # التحقق من عدد الصفوف المتأثرة
        if cursor.rowcount == 0:
            return jsonify({"error": "Note not found"}), 404

        cursor.close()
        db.close()

        return jsonify({
            "message": "Note deleted successfully",
            "id": note_id
        })

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))  # لو Railway حدد بورت، هنستخدمه
    app.run(host="0.0.0.0", port=port, debug=True)

