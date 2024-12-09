import uuid
import json

from runner.adapters import serializers
from runner.domain import model


def test_job_json_encoder():
    jobid = str(uuid.uuid4())
    job_dict = {
        "id": jobid,
        "state": "init",
        "instructions": [("open_file", {"path": "/fake/path"})],
    }

    expected_json = f"""
    {{
        "id": "{jobid}",
        "state": "init",
        "instructions": [["open_file", {{"path": "/fake/path"}}]],
        "version": 1
    }}
    """

    job = model.Job.from_dict(job_dict)
    json_str = json.dumps(job, cls=serializers.JobJsonEncoder)
    assert json.loads(json_str) == json.loads(expected_json)
