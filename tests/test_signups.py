def test_signup_adds_student_to_activity(client):
    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": "student@example.edu"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up student@example.edu for Chess Club"
    }

    activities = client.get("/activities").json()
    assert "student@example.edu" in activities["Chess Club"]["participants"]


def test_signup_for_unknown_activity_returns_not_found(client):
    response = client.post(
        "/activities/Unknown/signup", params={"email": "student@example.edu"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_duplicate_signup_returns_bad_request(client):
    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": "michael@mergington.edu"}
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_cancel_signup_removes_student_from_activity(client):
    response = client.delete(
        "/activities/Chess%20Club/signup", params={"email": "michael@mergington.edu"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Cancelled signup for michael@mergington.edu in Chess Club"
    }

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_cancel_signup_for_unknown_activity_returns_not_found(client):
    response = client.delete(
        "/activities/Unknown/signup", params={"email": "student@example.edu"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_cancel_signup_for_unenrolled_student_returns_not_found(client):
    response = client.delete(
        "/activities/Chess%20Club/signup", params={"email": "student@example.edu"}
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }