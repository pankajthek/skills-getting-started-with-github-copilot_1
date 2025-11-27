import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_list_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_and_unregister():
    # Use a test activity and email
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"

    # Sign up
    signup_url = f"/activities/{activity}/signup?email={email}"
    response = client.post(signup_url)
    assert response.status_code == 200
    assert "success" in response.json()["message"].lower()

    # Unregister
    unregister_url = f"/activities/{activity}/unregister?email={email}"
    response = client.post(unregister_url)
    assert response.status_code == 200
    assert "success" in response.json()["message"].lower()


def test_signup_invalid_activity():
    response = client.post("/activities/invalid_activity/signup?email=test@mergington.edu")
    assert response.status_code == 404


def test_signup_missing_email():
    activity = list(client.get("/activities").json().keys())[0]
    response = client.post(f"/activities/{activity}/signup?email=")
    assert response.status_code == 400
