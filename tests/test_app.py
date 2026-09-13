from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_signup_rejects_duplicate_email():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate-check@mergington.edu"
    activities[activity_name]["participants"] = [
        participant for participant in activities[activity_name]["participants"] if participant != email
    ]

    # Act
    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up for this activity"
    assert activities[activity_name]["participants"].count(email) == 1


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Programming Class"
    email = "remove-me@mergington.edu"
    activities[activity_name]["participants"] = [
        participant for participant in activities[activity_name]["participants"] if participant != email
    ]

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert before unregister
    assert signup_response.status_code == 200
    assert email in activities[activity_name]["participants"]

    # Act again
    unregister_response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert final state
    assert unregister_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
