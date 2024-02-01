import pytest
import json

from runner.entrypoints.flask_app import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_api(client):
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json == {"message": "Hello, World!"}


def test_happy_path_returns_201_and_execute_instruction(client):
    json_data = '{"instructions": [["example_script", {"data": 123}], ["example_script", {"data": 50}]], "dispatcher": "local"}'
    r = client.post("/execute", json=json.loads(json_data))

    assert r.status_code == 201
    assert r.json["message"] == "success"


def test_unhappy_path_returns_400_and_error_message(client):
    json_data = '{"instructions": [["nonexisting_script", {"data": 50}]], "dispatcher": "local"}'
    r = client.post("/execute", json=json.loads(json_data))

    assert r.status_code == 400
    assert (
        f"ScriptNotFoundError: Script file nonexisting_script.py does not exist."
        == r.json["message"]
    )
