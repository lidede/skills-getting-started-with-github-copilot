from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_successfully_adds_participant(client):
    activity = "Chess Club"
    email = "new.student@mergington.edu"

    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in activities[activity]["participants"]


def test_signup_activity_not_found_returns_404(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "a@b.com"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity}/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_when_activity_is_full_returns_400(client):
    activity = "Debate Team"
    activities[activity]["participants"] = [
        f"student{i}@mergington.edu" for i in range(activities[activity]["max_participants"])
    ]

    response = client.post(
        f"/activities/{activity}/signup", params={"email": "extra.student@mergington.edu"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is at maximum capacity"


def test_unregister_successfully_removes_participant(client):
    activity = "Gym Class"
    email = "john@mergington.edu"

    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in activities[activity]["participants"]


def test_unregister_activity_not_found_returns_404(client):
    response = client.delete("/activities/Unknown%20Club/signup", params={"email": "a@b.com"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_participant_returns_404(client):
    activity = "Basketball Team"
    email = "not.registered@mergington.edu"

    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
