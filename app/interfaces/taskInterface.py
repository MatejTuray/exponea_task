from functools import wraps


def add_runner(source, runner_type):
    def task_decorator(f, *args, **kwargs):
        @wraps(f, *args, **kwargs)
        def decorated(self, *args, **kwargs):
            factory = source.value
            runner = factory().create_runner(runner_type.name)
            self.runners.push(runner)
            return f(self, *args, **kwargs)

        return decorated

    return task_decorator
