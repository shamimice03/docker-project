from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")
EC2_PUBLIC_URL = os.environ.get("EC2_PUBLIC_URL", "localhost")


@app.route("/", methods=["GET"])
def home():
    return render_template("AddEmp.html", ec2_public_url=EC2_PUBLIC_URL)


@app.route("/AddEmp", methods=["POST"])
def add_employee():
    employee_data = {
        "emp_id": request.form.get("emp_id"),
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "pri_skill": request.form.get("pri_skill"),
        "location": request.form.get("location"),
    }

    try:
        response = requests.post(f"{BACKEND_URL}/api/employee", json=employee_data)
        if response.status_code == 201:
            return render_template(
                "AddEmpOutput.html",
                name=f"{employee_data['first_name']} {employee_data['last_name']}",
            )
        else:
            error_message = response.json().get("error", "Unknown error occurred")
            return f"An error occurred while adding the employee: {error_message}", 500
    except requests.RequestException as e:
        print(f"Error connecting to backend: {str(e)}")
        return f"An error occurred while connecting to the server: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))
