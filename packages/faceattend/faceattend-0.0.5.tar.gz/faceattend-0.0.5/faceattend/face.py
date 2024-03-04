from face_recognition import (
    face_encodings,
    load_image_file,
    face_locations,
)
import sqlite3
import numpy as np
import random


# generate a random 10 digit number for emp id
def generate_emp_id():
    return str(random.randint(1000000000, 9999999999))


def connect():
    """Returns a connection object"""
    return sqlite3.connect("valid_persons.db")


class Face:
    # add the face encoding bytes to the database for the specific person
    @staticmethod
    def add_face(name, img_file):
        if not img_file:
            return "An image file is required!"
        if not name:
            return "Name is required!"
        try:
            img = load_image_file(img_file)
        except FileNotFoundError:
            return f"Wrong Path or file name! No such file as '{img_file}'"
        faceloc = face_locations(img)
        face_encode = face_encodings(img, faceloc, 1)[0]
        emp_id = generate_emp_id()
        con = connect()
        cur = con.cursor()
        try:
            cur.execute(
                "INSERT INTO persons (name,emp_id,face_encoding) VALUES(?,?,?)",
                (name, emp_id, face_encode.tobytes()),
            )
            con.commit()
            con.close()
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
        return f"Person with {emp_id} has been removed!"

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
