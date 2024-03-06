import sqlite3


def create_database():
    conn = sqlite3.connect("valid_persons.db")
    conn.cursor().execute(
        """CREATE TABLE IF NOT EXISTS persons(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    emp_id TEXT NOT NULL,
    face_encoding BLOB UNIQUE NOT NULL
    )"""
    )
    conn.cursor().execute(
        """CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    person_id INTEGER NOT NULL,
    FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
    )"""
    )
    conn.close()
    return "Database created!"


if __name__ == "__main__":
    create_database()
