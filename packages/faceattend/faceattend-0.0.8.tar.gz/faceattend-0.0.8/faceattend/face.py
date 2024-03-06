from face_recognition import (
    face_encodings,
    load_image_file,
    face_locations,
)
import sqlite3
import numpy as np
import random
import os
import csv
import smtplib
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError


# generate a random 10 digit number for emp id
def generate_emp_id():
    return str(random.randint(1000000000, 9999999999))


# Send an email to the employee
def send_email(name, emp_id, email):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        msg = EmailMessage()
        msg.set_content(
            f"Hello {name},\n\nWe're delighted to inform you that you have been successfully registered in our system.\n\nYour employee ID is: {emp_id}.\n\nThank you for joining us!\n\nBest regards,\nThe Team"
        )
        msg["Subject"] = "Successfully Registered!"
        msg["From"] = os.environ["mail_user"]
        msg["To"] = email
        smtp.login(os.environ["mail_user"], os.environ["mail_password"])
        smtp.send_message(msg)


def connect():
    """Returns a connection object"""
    if not os.path.isfile("valid_persons.db"):
        return False
    return sqlite3.connect("valid_persons.db", check_same_thread=True)


class Face:
    # Add the face encoding bytes to the database for the specific person
    @staticmethod
    def add_face(name, email, img_file):
        if not img_file:
            return "An image file is required!"
        if not name:
            return "Name is required!"
        try:
            email = validate_email(email, check_deliverability=True)
        except EmailNotValidError as e:
            return str(e)
        try:
            img = load_image_file(img_file)
        except FileNotFoundError:
            return f"Wrong Path or file name! No such file as '{img_file}'"
        faceloc = face_locations(img)
        face_encode = face_encodings(img, faceloc, 1)[0]
        emp_id = generate_emp_id()
        con = connect()
        if not con:
            return "Create database first"
        cur = con.cursor()
        try:
            cur.execute(
                "INSERT INTO persons (name,email,emp_id,face_encoding) VALUES(?,?,?,?)",
                (name, email.normalized, emp_id, face_encode.tobytes()),
            )
            con.commit()
            con.close()
            send_email(name, emp_id, email.normalized)
            return f"Face added for {name} with employee id {emp_id}"
        except sqlite3.IntegrityError:
            return "Face already exists!"

    # Delete the person from database given its emp id
    @staticmethod
    def delete_face(emp_id):
        con = connect()
        cur = con.cursor()
        cur.execute("SELECT * FROM persons WHERE emp_id = ?", (emp_id,))
        if not cur.fetchone():
            return f"No person with emp id of {emp_id} was found!"
        cur.execute("DELETE FROM persons WHERE emp_id = ?", (emp_id,))
        con.commit()
        con.close()
        return f"Person with emp_id {emp_id} has been removed!"

    # read all the face_encodings and names from the database and return and list containg all the known face_encodings and name
    @staticmethod
    def load_faces():
        con = connect()
        cur = con.cursor()
        cur.execute("SELECT name,face_encoding FROM persons")
        encodings = cur.fetchall()
        known_face_encodings = [encoding[1] for encoding in encodings]
        known_face_names = [name[0] for name in encodings]
        known_face_encodings = [
            np.frombuffer(encoding, dtype="float64")
            for encoding in known_face_encodings
        ]
        con.close()
        return known_face_encodings, known_face_names

    # generate a csv file containing all the persons in the database
    @staticmethod
    def generate_emp_list():
        con = connect()
        cur = con.cursor()
        cur.execute("SELECT id,name,email,emp_id FROM persons")
        persons = cur.fetchall()
        if not persons:
            return "No data available!"
        os.makedirs("csv/", exist_ok=True)
        with open("csv/employee_list.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["No", "Name", "Email", "Emp_id"])
            writer.writerows(persons)
        con.close()
        return "CSV file generated!"
