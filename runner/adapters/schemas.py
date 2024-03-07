from schema import Schema, Optional


job_schema = Schema(
    {"id": str, Optional("state"): str, "instructions": list}, ignore_extra_keys=True
)
