import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


def test_unregister_participant_removes_the_student_from_the_activity():
    client = TestClient(app)

    signup_response = client.post(
        "/activities/Chess Club/signup?email=student@example.com"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        "/activities/Chess Club/unregister?email=student@example.com"
    )
    assert unregister_response.status_code == 200

    activity_data = client.get("/activities").json()["Chess Club"]
    assert "student@example.com" not in activity_data["participants"]
