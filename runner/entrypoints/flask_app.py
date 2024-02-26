import json
import uuid
from flask import Flask, request, jsonify

from runner.domain import model
from runner.adapters import repository, executer
from runner.service_layer import job_services, unit_of_work


app = Flask(__name__)


JOB_UOW = unit_of_work.FileSystemJobUnitOfWork()
SCRIPT_REPO = repository.FileSystemRepository()
EXECUTER = executer.LocalExecuter(SCRIPT_REPO)


@app.route("/execute", methods=["POST"])
def execute_endpoint():
    jobid = str(uuid.uuid4())

    job_services.add(jobid, request.json["instructions"], JOB_UOW)
    job_services.execute(jobid=jobid, job_uow=JOB_UOW, executer=EXECUTER)

    with JOB_UOW:
        job = JOB_UOW.jobs.get(jobid)

    if job.state == "failed":
        return {"message": "failed", "job_id": jobid}, 400

    return {"message": "success", "job_id": jobid}, 201


@app.route("/api", methods=["GET"])
def my_api():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(debug=True)
