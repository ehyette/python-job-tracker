from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "data", "applications.csv")

FIELDNAMES = ["company", "job_title", "status", "notes"]


def load_applications():
    applications = []

    if not os.path.exists(CSV_FILE):
        return applications

    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            applications.append(row)

    return applications


def save_application(application):
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        if not file_exists:
            writer.writeheader()

        writer.writerow(application)

def save_all_applications(applications):
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(applications)


@app.route("/")
def home():
    search_query = request.args.get("search", "").lower()
    applications = load_applications()

    if search_query:
        applications = [
            application for application in applications
            if search_query in application["company"].lower()
            or search_query in application["job_title"].lower()
            or search_query in application["status"].lower()
            or search_query in application["notes"].lower()
        ]

    return render_template(
        "index.html",
        applications=applications,
        search_query=search_query
    )


@app.route("/add", methods=["POST"])
def add_application():
    new_application = {
        "company": request.form.get("company"),
        "job_title": request.form.get("job_title"),
        "status": request.form.get("status"),
        "notes": request.form.get("notes")
    }

    save_application(new_application)

    return redirect("/")

@app.route("/update_status/<int:index>", methods=["POST"])
def update_status(index):
    applications = load_applications()

    if 0 <= index < len(applications):
        applications[index]["status"] = request.form.get("status")
        save_all_applications(applications)

    return redirect("/")

@app.route("/delete/<int:index>", methods=["POST"])
def delete_application(index):
    applications = load_applications()

    if 0 <= index < len(applications):
        applications.pop(index)
        save_all_applications(applications)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)