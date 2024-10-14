from flask import Flask, jsonify
import pymysql
import os
import logging
import uuid

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)


def get_db_connection():
    logging.info("Establishing database connection.")
    return pymysql.connect(
        host=os.environ.get("DBHOST"),
        user=os.environ.get("DBUSER"),
        password=os.environ.get("DBPWD"),
        db=os.environ.get("DATABASE"),
        port=int(os.environ.get("DBPORT", 3306)),
    )


@app.route("/api/employee/<emp_id>", methods=["GET"])
def get_employee(emp_id):
    request_id = uuid.uuid4()  # Unique ID for tracking requests
    conn = None
    logging.info(f"Request ID {request_id}: Handling request for employee ID: {emp_id}")

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM Employee WHERE emp_id = %s"
            logging.info(
                f"Request ID {request_id}: Executing query: {sql} with emp_id: {emp_id}"
            )
            cursor.execute(sql, (emp_id,))
            result = cursor.fetchone()

            if result:
                employee = {
                    "emp_id": result[0],
                    "first_name": result[1],
                    "last_name": result[2],
                    "pri_skill": result[3],
                    "location": result[4],
                }
                logging.info(f"Request ID {request_id}: Employee found: {employee}")
                return jsonify(employee), 200
            else:
                logging.warning(
                    f"Request ID {request_id}: Employee not found for ID: {emp_id}"
                )
                return jsonify({"error": "Employee not found"}), 404
    except Exception as e:
        logging.error(f"Request ID {request_id}: Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()
            logging.info(f"Request ID {request_id}: Database connection closed.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))
