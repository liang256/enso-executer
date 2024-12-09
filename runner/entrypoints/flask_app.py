from flask import Flask, request, jsonify
from flasgger import Swagger
from runner.service_layer import services, unit_of_work
from runner.adapters import job_repository

app = Flask(__name__)

# Initialize Flasgger
swagger = Swagger(app)

UNIT_OF_WORK = unit_of_work.InMemoryJobUnitOfWork()


@app.route("/add-job", methods=["POST"])
def add_job():
    """
    Add a new job.
    ---
    tags:
      - Job Management
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            instructions:
              type: array
              description: List of instructions, each containing a script and its arguments.
              items:
                type: array
                minItems: 2
                maxItems: 2
                items:
                  - type: string
                    description: Script name
                  - type: object
                    description: Dictionary of arguments for the script
    responses:
      201:
        description: Job added successfully
        schema:
          type: object
          properties:
            jobid:
              type: string
      400:
        description: Missing or invalid instructions
    """
    data = request.json
    instructions = data.get("instructions")
    if not instructions:
        return jsonify({"error": "Missing instructions"}), 400

    jobid = services.add(instructions, UNIT_OF_WORK)
    return jsonify({"jobid": jobid}), 201


@app.route("/list-jobs", methods=["GET"])
def list_jobs():
    """
    List all jobs.
    ---
    tags:
      - Job Management
    responses:
      200:
        description: A list of jobs
        schema:
          type: object
          properties:
            jobs:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    description: Unique identifier of the job
                  state:
                    type: string
                    description: Current state of the job
                  version:
                    type: integer
                    description: Version of the job
                  instructions:
                    type: array
                    description: List of instructions for the job
                    items:
                      type: object
                      properties:
                        script:
                          type: string
                          description: Name of the script
                        arguments:
                          type: object
                          additionalProperties:
                            type: string
                          description: Key-value arguments for the script
                  events:
                    type: array
                    description: List of events for the job execution
                    items:
                      type: string
                      description: Event description
    """
    jobs = UNIT_OF_WORK.jobs.list()
    return jsonify({"jobs": [job.to_dict() for job in jobs]})


@app.route("/get-job/<jobid>", methods=["GET"])
def get_job(jobid):
    """
    Get details of a specific job by ID.
    ---
    tags:
      - Job Management
    parameters:
      - in: path
        name: jobid
        required: true
        schema:
          type: string
        description: The ID of the job
    responses:
      200:
        description: Job details
        schema:
          type: object
          properties:
            id:
              type: string
              description: Unique identifier of the job
            state:
              type: string
              description: Current state of the job
            version:
              type: integer
              description: Version of the job
            instructions:
              type: array
              description: List of instructions for the job
              items:
                type: object
                properties:
                  script:
                    type: string
                    description: Name of the script
                  arguments:
                    type: object
                    additionalProperties:
                      type: string
                    description: Key-value arguments for the script
            events:
              type: array
              description: List of events for the job execution
              items:
                type: string
                description: Event description
      404:
        description: Job not found
    """
    job_dict = services.get(jobid, UNIT_OF_WORK)
    if not job_dict:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job_dict), 200


@app.route("/execute-job", methods=["POST"])
def execute_job():
    """
    Execute a job by ID.
    ---
    tags:
      - Job Management
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            jobid:
              type: string
              description: The ID of the job to execute
    responses:
      200:
        description: Job executed successfully
        schema:
          type: object
          properties:
            jobid:
              type: string
            message:
              type: string
      400:
        description: Job already executed or invalid jobid
      404:
        description: Job not found
    """
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
