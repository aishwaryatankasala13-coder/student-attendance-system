
from app import app


def test_home_page():
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Student Attendance Management System" in response.data


def test_add_student_page():
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/add-student")

    assert response.status_code == 200
