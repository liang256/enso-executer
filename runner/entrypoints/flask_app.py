from flask import Flask, request, jsonify
from runner.service_layer import services, unit_of_work
from runner.adapters import serializers

app = Flask(__name__)
app.json_encoder = serializers.JobJsonEncoder

# 假資料庫（使用內存暫存數據）
people = []
UNIT_OF_WORK = unit_of_work.InMemoryJobUnitOfWork()

@app.route("/add", methods=["POST"])
def add_person():
    data = request.json
    name = data.get("name")
    age = data.get("age")
    height = data.get("height")

    if not name or not age or not height:
        return jsonify({"error": "Missing fields"}), 400

    person = {"name": name, "age": age, "height": height}
    people.append(person)
    return jsonify({"message": "Person added", "person": person}), 201


@app.route("/list", methods=["GET"])
def list_people():
    return jsonify({"people": people})

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
