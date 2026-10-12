
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "attendance_db")
    )


@app.route("/")
def home():
    return """
    <h1>Student Attendance Management System</h1>
    <ul>
        <li><a href="/add-student">Add Student</a></li>
        <li><a href="/mark-attendance">Mark Attendance</a></li>
        <li><a href="/attendance">View Attendance</a></li>
        <li><a href="/percentage">Attendance Percentage</a></li>
    </ul>
    """


@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        roll_number = request.form["roll_number"]
        email = request.form["email"]
        department = request.form["department"]

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO students (name, roll_number, email, department)
            VALUES (%s, %s, %s, %s)
            """,
            (name, roll_number, email, department)
        )

        connection.commit()
        cursor.close()
        connection.close()

        return """
        Student added successfully!
        <br><a href="/add-student">Add another student</a>
        <br><a href="/">Home</a>
        """

    return render_template("add_student.html")


@app.route("/mark-attendance", methods=["GET", "POST"])
def mark_attendance():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        student_id = request.form["student_id"]
        attendance_date = request.form["attendance_date"]
        status = request.form["status"]

        cursor.execute(
            """
            INSERT INTO attendance (student_id, attendance_date, status)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE status = %s
            """,
            (student_id, attendance_date, status, status)
        )

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for("attendance_records"))

    cursor.execute("SELECT id, name, roll_number FROM students")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("mark_attendance.html", students=students)


@app.route("/attendance")
def attendance_records():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT s.name, s.roll_number,
               a.attendance_date, a.status
        FROM attendance a
        JOIN students s ON s.id = a.student_id
        ORDER BY a.attendance_date DESC
        """
    )

    records = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("attendance.html", records=records)


@app.route("/percentage")
def percentage():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT s.id, s.name, s.roll_number,
               COUNT(a.id) AS total_days,
               COALESCE(SUM(a.status = 'Present'), 0) AS present_days
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
        GROUP BY s.id, s.name, s.roll_number
        ORDER BY s.roll_number
        """
    )

    students = cursor.fetchall()

    for student in students:
        total = student["total_days"]
        present = student["present_days"]
        student["percentage"] = round(present / total * 100, 2) if total else 0

    cursor.close()
    connection.close()

    return render_template("percentage.html", students=students)


if __name__ == "__main__":
    app.run(debug=True)
