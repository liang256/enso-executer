import json
from flask import Flask, request, jsonify

from runner.domain import model
from runner.adapters import repository, dispatcher
from runner.service_layer import services


app = Flask(__name__)


@app.route("/execute", methods=["POST"])
def execute_endpoint():
    if "local" not in request.json["dispatcher"].lower():
        return {"message": f"Invalid dispatcher: {request.json['dispatcher']}"}, 400

    try:
        services.execute(
            request.json["instructions"],
            repository.FileSystemRepository(),
            dispatcher.LocalDispathcer(),
        )
    except (
        json.decoder.JSONDecodeError,
        model.MissingRequiredArguments,
        repository.ScriptNotFoundError,
        repository.LoadScriptError,
    ) as e:
        return {"message": f"{e.__class__.__name__}: {str(e)}"}, 400

    return {"message": "success"}, 201


@app.route("/api", methods=["GET"])
def my_api():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(debug=True)
