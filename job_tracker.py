import csv
import os

applications = []
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "data", "applications.csv")

# Shows initial Menu to user

def show_menu():
    print("\nJob Application Tracker")
    print("1. Add job application")
    print("2. View all applications")
    print("3. Search applications")
    print("4. Update application status")
    print("5. Delete application")
    print("6. Exit")

# Saves applications to CSV file

def save_applications():
    os.makedirs(os.path.dirname(FILE_NAME), exist_ok=True)

    with open(FILE_NAME, "w", newline="") as file:
        fieldnames = ["company", "job_title", "location", "date_applied", "status", "job_link", "notes"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(applications)

# Loads applications from CSV file

def load_applications():
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                applications.append(row)

    except FileNotFoundError:
        pass

# Allows the user to add a job 

def get_input(prompt):
    user_input = input(prompt)

    if user_input.lower() == "cancel":
        return None

    return user_input


def add_job():
    print("\nAdd Job Application")
    print("Type 'cancel' at any time to return to the main menu.")

    company = get_input("Company name: ")
    if company is None:
        print("\nAdd job cancelled.")
        return

    job_title = get_input("Job title: ")
    if job_title is None:
        print("\nAdd job cancelled.")
        return

    location = get_input("Location: ")
    if location is None:
        print("\nAdd job cancelled.")
        return

    date_applied = get_input("Date applied: ")
    if date_applied is None:
        print("\nAdd job cancelled.")
        return

    status = get_input("Status: ")
    if status is None:
        print("\nAdd job cancelled.")
        return

    job_link = get_input("Job link: ")
    if job_link is None:
        print("\nAdd job cancelled.")
        return

    notes = get_input("Notes: ")
    if notes is None:
        print("\nAdd job cancelled.")
        return

    job = {
        "company": company,
        "job_title": job_title,
        "location": location,
        "date_applied": date_applied,
        "status": status,
        "job_link": job_link,
        "notes": notes
    }

    applications.append(job)
    save_applications()

    print("\nJob added successfully!")
    print(f"{job_title} at {company}")

# Allows the user to view all applications

def view_applications():
    if len(applications) == 0:
        print("\nNo job applications found.")
    else:
        print("\nAll Job Applications:")

        for job in applications:
            print("-------------------------")
            print(f"Company: {job['company']}")
            print(f"Job Title: {job['job_title']}")
            print(f"Location: {job['location']}")
            print(f"Date Applied: {job['date_applied']}")
            print(f"Status: {job['status']}")
            print(f"Job Link: {job['job_link']}")
            print(f"Notes: {job['notes']}")

# Allows the user to search for applications by any field

def search_applications():
    search_term = input("Enter company or job title to search: ").lower()
    found = False

    if len(applications) == 0:
        print("\nNo job applications found.")
    else:
        for job in applications:
            if search_term in job["company"].lower() or search_term in job["job_title"].lower():
                found = True


                print("-------------------------")
                print(f"Company: {job['company']}")
                print(f"Job Title: {job['job_title']}")
                print(f"Location: {job['location']}")
                print(f"Date Applied: {job['date_applied']}")
                print(f"Status: {job['status']}")
                print(f"Job Link: {job['job_link']}")
                print(f"Notes: {job['notes']}")
            
        if not found:
            print("\nNo matching applications found.")

# Allows the user to update the status of an application

def update_status():
    if len(applications) == 0:
        print("\nNo job applications found.")
    else:
        print("\nWhich application do you want to update?")

        for index, job in enumerate(applications):
            print(f"{index + 1}. {job['job_title']} at {job['company']} - Current Status: {job['status']}")

        choice = input("Enter the application number: ")

        if choice.isdigit():
            choice = int(choice)

            if choice >= 1 and choice <= len(applications):
                new_status = input("Enter new status: ")

                applications[choice - 1]["status"] = new_status
                save_applications()

                print("\nStatus updated successfully!")
                print(f"New status: {new_status}")
            else:
                print("\nInvalid application number.")
        else:
            print("\nPlease enter a valid number.")

# Allows the user to delete an application

def delete_application():
    if len(applications) == 0:
        print("\nNo job applications found.")
    else:
        print("\nWhich application do you want to delete?")

        for index, job in enumerate(applications):
            print(f"{index + 1}. {job['job_title']} at {job['company']} - Status: {job['status']}")

        choice = input("Enter the application number to delete: ")

        if choice.isdigit():
            choice = int(choice)

            if choice >= 1 and choice <= len(applications):
                removed_job = applications.pop(choice - 1)
                save_applications()

                print("\nApplication deleted successfully!")
                print(f"Deleted: {removed_job['job_title']} at {removed_job['company']}")
            else:
                print("\nInvalid application number.")
        else:
            print("\nPlease enter a valid number.")


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            add_job()

        elif choice == "2":
            view_applications()

        elif choice == "3":
            search_applications()

        elif choice == "4":
            update_status()

        elif choice == "5":
            delete_application()

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Please choose 1-6.")

load_applications()
main()