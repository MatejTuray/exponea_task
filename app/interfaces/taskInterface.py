from functools import wraps


def add_runner(source, runner_type):
    def task_decorator(f, *args, **kwargs):
        @wraps(f, *args, **kwargs)
        def decorated(self, *args, **kwargs):
            creator = source.value
            runner = creator().create_runner(runner_type.name)
            self.runners.append(runner)
            return f(self, *args, **kwargs)

        return decorated

    return task_decorator
