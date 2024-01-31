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
    script_name = "example_script"
    args = {"file": "file/path"}
    data = {"script": script_name, "args": json.dumps(args), "dispatcher": "local"}
    r = client.post("/execute", json=data)

    assert r.status_code == 201
    assert r.json["message"] == "success"


def test_unhappy_path_returns_400_and_error_message(client):
    script_name = "nonexisting_script"
    data = {"script": script_name, "args": json.dumps({}), "dispatcher": "local"}
    r = client.post("/execute", json=data)

    assert r.status_code == 400
    assert (
        f"ScriptNotFoundError: Script file {script_name}.py does not exist."
        == r.json["message"]
    )
