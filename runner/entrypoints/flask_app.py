from flask import Flask, request, jsonify
from runner.service_layer import services, unit_of_work
from runner.adapters import job_repository

app = Flask(__name__)
UNIT_OF_WORK = unit_of_work.InMemoryJobUnitOfWork()


@app.route("/add-job", methods=["POST"])
def add_job():
    data = request.json
    instructions = data.get("instructions")
    if not instructions:
        return jsonify({"error": "Missing instructions"}), 400

    jobid = services.add(instructions, UNIT_OF_WORK)
    return jsonify({"jobid": jobid}), 201


@app.route("/list-jobs", methods=["GET"])
def list_jobs():
    jobs = UNIT_OF_WORK.jobs.list()
    return jsonify({"jobs": [job.to_dict() for job in jobs]})


@app.route("/get-job/<jobid>", methods=["GET"])
def get_job(jobid):
    job_dict = services.get(jobid, UNIT_OF_WORK)
    if not job_dict:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job_dict), 200


@app.route("/execute-job", methods=["POST"])
def execute_job():
    jobid = request.json.get("jobid")
    if not jobid:
        return jsonify({"error": "Missing jobid"}), 400

    try:
        services.execute(jobid, UNIT_OF_WORK)
    except services.JobHasCompleted as e:
        return jsonify({"error": str(e)}), 400
    except job_repository.JobNotFound:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({"jobid": jobid, "message": "Job executed"}), 200


if __name__ == "__main__":
    app.run(debug=True)
