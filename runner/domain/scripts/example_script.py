from runner.domain import model
from typing import Dict, Tuple


class ExampleScript(model.AbstractScript):
    def execute(self, args: Dict[str, str]) -> None:
        print(f"execute {self.__class__.__name__} with args: {args}")

    def get_required_args(self) -> Tuple[str, ...]:
        return tuple()

    @property
    def ref(self):
        return "example_script"
