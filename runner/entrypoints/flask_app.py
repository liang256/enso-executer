import json
from flask import Flask, request, jsonify

from runner.domain import model
from runner.adapters import repository, executer
from runner.service_layer import job_services


app = Flask(__name__)


class FakeSession:
    def commit(self):
        pass


class FakeJobRepo(dict):
    def add(self, job):
        self[job.id] = job


SESSION = FakeSession()
JOB_REPO = FakeJobRepo()
SCRIPT_REPO = repository.FileSystemRepository()
EXECUTER = executer.LocalExecuter(SCRIPT_REPO)


@app.route("/execute", methods=["POST"])
def execute_endpoint():
    if "local" not in request.json["dispatcher"].lower():
        return {"message": f"Invalid dispatcher: {request.json['dispatcher']}"}, 400

    try:
        jobid = job_services.add(request.json["instructions"], JOB_REPO, SESSION)
    except (
        json.decoder.JSONDecodeError,
        # model.MissingRequiredArguments,
        # repository.ScriptNotFoundError,
        # repository.LoadScriptError,
    ) as e:
        return {"message": f"{e.__class__.__name__}: {str(e)}"}, 400

    job_services.execute(
        jobid=jobid, job_repo=JOB_REPO, executer=EXECUTER, session=SESSION
    )

    job = JOB_REPO.get(jobid)

    if job.state == "failed":
        return {"message": "failed", "job_id": jobid}, 400

    return {"message": "success", "job_id": jobid}, 201


@app.route("/api", methods=["GET"])
def my_api():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(debug=True)
