from runner.domain import model
from typing import Tuple, Dict
import pytest


class FakeScript(model.AbstractScript):
    ref = "fake_script"
    required_args = ("name", "age")

    def execute(self, args: Dict) -> None:
        pass


def test_error_for_invalid_args():
    script = FakeScript()
    excepted_error_msg = "Missing required arguments in FakeScript: name, age"

    with pytest.raises(model.MissingRequiredArguments, match=excepted_error_msg):
        model.validate_args(script, {})


def test_get_missing_args():
    reqs = ("name", "age", "gender")
    args = {"name": "Amy", "age": 18, "hobby": "reading"}
    expected_res = ["gender"]
    assert expected_res == list(model.get_missing_args(reqs, args))
