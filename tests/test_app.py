import pytest
from fastapi.testclient import TestClient
from fastapi import status
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert f"Signed up {test_email}" in response.json().get("message", "")

def test_signup_duplicate():
    # Arrange
    test_email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already signed up" in response.json().get("detail", "")

def test_signup_activity_not_found():
    # Arrange
    test_email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Activity not found" in response.json().get("detail", "")

# Note: Unregister endpoint is not implemented yet. Add tests when available.
