from runner.domain import model


class ExampleScript(model.AbstractScript):
    ref = "example_script"
    required_args = tuple()

    def execute(self, **kwargs) -> None:
        print(f"execute {self.__class__.__name__} with args: {kwargs}")
