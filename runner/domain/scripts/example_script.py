from runner.domain import model
from typing import Dict


class ExampleScript(model.AbstractScript):
    ref = "example_script"
    required_args = tuple()

    def execute(self, args: Dict) -> None:
        print(f"execute {self.__class__.__name__} with args: {args}")
