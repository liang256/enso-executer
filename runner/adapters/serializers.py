import json

from runner.domain import model


class JobJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, model.Job):
            return {
                "id": o.id,
                "version": o.version,
                "instructions": o.instructions,
                "state": o.state,
            }
        return super().default(o)
