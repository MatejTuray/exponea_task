import itertools
import abc
from concurrent.futures import (
    ThreadPoolExecutor,
    wait,
    ALL_COMPLETED,
    FIRST_COMPLETED,
)
from app.interfaces.taskInterface import TaskTypes
from app.interfaces.runnerFactory import AbstractRunner

class AllRunner:
    pass

class FirstRunner:
    pass

class TimeoutRunner:
    pass

class SmartRunner:
    pass

class Runner:
    def __init__(self):
        super().__init__()
        self.tasks = []

    def push_task(self, task, amount=1):
        self.tasks.extend([task] * amount)

    def schedule_tasks(self, task_count):
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(perform, task)
                for task in itertools.islice(self.tasks, task_count)
            }
