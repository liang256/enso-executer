from flask import Flask, request, jsonify
from runner.service_layer import services, unit_of_work

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


if __name__ == "__main__":
    app.run(debug=True)
