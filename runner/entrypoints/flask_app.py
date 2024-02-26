import json
import uuid
from flask import Flask, request, jsonify

from runner.domain import model
from runner.adapters import repository, executer
from runner.service_layer import job_services, unit_of_work


app = Flask(__name__)


JOB_UOW = unit_of_work.FileSystemJobUnitOfWork()
SCRIPT_REPO = repository.FileSystemRepository()
EXECUTER = executer.SimpleExecuter(SCRIPT_REPO)


@app.route("/jobs", methods=["POST"])
def add_job():
    try:
        jobid = job_services.add(request.json["instructions"], JOB_UOW)
    except Exception:
        return {"message": "failed"}, 400
    return {"message": "success", "job_id": jobid}, 201


@app.route("/execute", methods=["POST"])
def execute_endpoint():
    try:
        job_services.execute(
            jobid=request.json["job_id"], job_uow=JOB_UOW, executer=EXECUTER
        )
    except Exception:
        return {"message": "failed"}, 400
    return {"message": "success"}, 201


@app.route("/api", methods=["GET"])
def my_api():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(debug=True)
