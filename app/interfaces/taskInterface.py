from logger import log
from functools import wraps


def add_runner(source, runner_type):
    def task_decorator(f):
        @wraps(f)
        def decorated(self, *args, **kwargs):
            factory = source.value
            runner = factory.get_runner(runner_type.name)
            kwargs[f"{source.name}_{runner_type.name}"] = runner
            return f(self, *args, **kwargs)

        return decorated

    return task_decorator
