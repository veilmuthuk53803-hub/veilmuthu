from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert data["service"] == "EduGenie"


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_empty_request():

    response = client.post(
        "/qa",
        json={
            "text": ""
        },
    )

    assert response.status_code == 422
