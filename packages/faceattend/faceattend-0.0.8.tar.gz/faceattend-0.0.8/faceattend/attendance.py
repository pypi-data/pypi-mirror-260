import sqlite3
import csv
from datetime import datetime, date
from gtts import gTTS
from pygame import mixer
import os


def connect():
    """Returns a connection object"""
    return sqlite3.connect("valid_persons.db")


class Attendance:
    # Returns True if already marked and False if not marked
    @staticmethod
    def if_marked(face_encoding):
        con = connect()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM attendance WHERE date = ? AND person_id = (SELECT id FROM persons WHERE face_encoding = ?)",
            (datetime.today().strftime("%Y-%m-%d"), face_encoding.tobytes()),
        )
        if not cur.fetchone():
            return False
        else:
            return True

    # mark attendance of a detected person
    @staticmethod
    def mark_attendance(face_encodings: list):
        con = connect()
        cur = con.cursor()
        if face_encodings:
            for encoding in face_encodings:
                if Attendance.if_marked(encoding) == False:
                    cur.execute(
                        "SELECT id,name from persons WHERE face_encoding = ?",
                        (encoding.tobytes(),),
                    )
                    result = cur.fetchone()
                    name = result[1]
                    person_id = result[0]
                    cur.execute(
                        "INSERT INTO attendance(date,person_id) VALUES(?,?)",
                        (datetime.today().strftime("%Y-%m-%d"), person_id),
                    )
                    con.commit()
                    con.close()
                    Attendance.give_feedback(f"{name} your attendance has been noted")

    # generate a csv with the attendance for a particular date
    @staticmethod
    def generate_csv_date(date_for_attendance):
        try:
            date.fromisoformat(date_for_attendance)
        except ValueError:
            return "Wrong date format!"
        con = connect()
        cur = con.cursor()
        cur.execute(
            "SELECT name,emp_id FROM persons WHERE id IN(SELECT person_id FROM attendance WHERE date = ?)",
            (date_for_attendance,),
        )
        results = cur.fetchall()
        if not results:
            return f"No data available for {date_for_attendance}"
        os.makedirs("csv/", exist_ok=True)
        with open(f"csv/{date_for_attendance}.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Emp_id"])
            writer.writerows(results)
        con.close()
        return "CSV file generated!"

    # generate a csv with the attendance for a particular employee
    @staticmethod
    def generate_csv_emp(emp_id):
        emp_id = str(emp_id)
        con = connect()
        cur = con.cursor()
        cur.execute("SELECT * FROM persons WHERE emp_id =?", (emp_id,))
        if not cur.fetchone():
            return f"No person with emp id {emp_id} exists"
        cur.execute(
            "SELECT date FROM attendance WHERE person_id = (SELECT id FROM persons WHERE emp_id = ?)",
            (emp_id,),
        )
        results = cur.fetchall()
        if not results:
            return f"No data available for employee with id {emp_id}"
        os.makedirs("csv/", exist_ok=True)
        with open(f"csv/{emp_id}.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date"])
            writer.writerows(results)
        con.close()
        return "CSV file generated!"

    # play the feedback sound
    @staticmethod
    def give_feedback(text):
        tts = gTTS(text)
        tts.save("feedback.mp3")
        mixer.init()
        sound = mixer.Sound("feedback.mp3")
        sound.play()
        os.remove("feedback.mp3")
