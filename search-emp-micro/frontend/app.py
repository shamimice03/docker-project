from flask import Flask, render_template, request
import requests
import os
import logging
import uuid

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set the backend URL
BACKEND_URL = os.environ.get("BACKEND_URL", "http://search-backend:5050")
EC2_PUBLIC_URL = os.environ.get("EC2_PUBLIC_URL", "localhost")


@app.route("/", methods=["GET"])
def home():
    return render_template("GetEmp.html", ec2_public_url=EC2_PUBLIC_URL)


@app.route("/GetEmp", methods=["POST"])
def get_employee():
    emp_id = request.form.get("emp_id")
    request_id = uuid.uuid4()  # Unique ID for tracking requests
    logging.info(f"Request ID {request_id}: Received request for employee ID: {emp_id}")

    try:
        response = requests.get(f"{BACKEND_URL}/api/employee/{emp_id}")
        logging.info(
            f"Request ID {request_id}: Requesting for employee ID {emp_id}: {response}"
        )

        if response.status_code == 200:
            employee = response.json()
            logging.info(f"Request ID {request_id}: Employee found: {employee}")
            return render_template("GetEmpOutput.html", employee=employee)
        elif response.status_code == 404:
            logging.warning(
                f"Request ID {request_id}: Employee not found for ID: {emp_id}"
            )
            return f"Employee not found", 404
        else:
            error_message = response.json().get("error", "Unknown error")
            logging.error(f"Request ID {request_id}: Error occurred: {error_message}")
            return (
                f"An error occurred while searching for the employee: {error_message}",
                500,
            )
    except requests.RequestException as e:
        logging.error(
            f"Request ID {request_id}: Error occurred while connecting to the server: {str(e)}"
        )
        return f"An error occurred while connecting to the server: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))
