from flask import Flask, request, jsonify
import pymysql
import os
import traceback

app = Flask(__name__)


def get_db_connection():
    try:
        return pymysql.connect(
            host=os.environ.get("DBHOST"),
            user=os.environ.get("DBUSER"),
            password=os.environ.get("DBPWD"),
            db=os.environ.get("DATABASE"),
            port=int(os.environ.get("DBPORT", 3306)),
        )
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise


@app.route("/api/employee", methods=["POST"])
def add_employee():
    data = request.json
    emp_id = data.get("emp_id")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    pri_skill = data.get("pri_skill")
    location = data.get("location")

    insert_sql = "INSERT INTO Employee VALUES (%s, %s, %s, %s, %s)"
    conn = None

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                insert_sql, (emp_id, first_name, last_name, pri_skill, location)
            )
        conn.commit()
        return (
            jsonify(
                {
                    "message": "Employee added successfully",
                    "name": f"{first_name} {last_name}",
                }
            ),
            201,
        )
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error adding employee: {str(e)}\n{error_details}")
        return (
            jsonify(
                {"error": f"An error occurred while adding the employee: {str(e)}"}
            ),
            500,
        )
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
