import itertools
from concurrent.futures import (
    ALL_COMPLETED,
    FIRST_COMPLETED,
    ThreadPoolExecutor,
    wait,
)
from interfaces.runnerInterface import AbstractRunner
from logger import log
from stopit import ThreadingTimeout


class BaseRunner(AbstractRunner):
    def __init__(self):
        super().__init__()
        self.tasks = []

    def push_task(self, task, task_args=[None], amount=1):
        self.tasks.extend([{"task": task, "args": task_args}] * amount)

    def schedule_tasks():
        raise NotImplementedError


class FirstRunner(BaseRunner):
    def schedule_tasks(self, task_count, timeout):
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(item["task"]): item["task"]
                for item in itertools.islice(iter(self.tasks), task_count)
            }
            while futures:
                done, _ = wait(
                    futures, timeout=timeout, return_when=FIRST_COMPLETED
                )

                for fut in done:
                    futures.pop(fut)
                    if type(fut.result()) == dict:
                        executor.shutdown(wait=False)
                        return fut.result()


class SmartRunner(BaseRunner):
    def schedule_tasks(self, task_count, timeout):
        with ThreadingTimeout(timeout, swallow_exc=False) as func_timeout:
            futures = {}
            with ThreadPoolExecutor() as executor:
                for item in itertools.islice(iter(self.tasks), task_count):
                    futures.update(
                        {executor.submit(item["task"]): item["task"]}
                    )
                self.tasks = []
                log.info(futures)
                while futures:
                    log.info(len(futures) == 2)
                    done, running = wait(
                        futures, timeout=timeout, return_when=FIRST_COMPLETED
                    )
                    for fut in done:
                        futures.pop(fut)
                        if type(fut.result()) == dict:
                            executor.shutdown(wait=False)
                            return fut.result()


class AllRunner(BaseRunner):
    def schedule_tasks(self, task_count, timeout):
        with ThreadPoolExecutor() as executor:
            result = []
            futures = {
                executor.submit(item["task"]): item["task"]
                for item in itertools.islice(iter(self.tasks), task_count)
            }
            while futures:
                done, _ = wait(
                    futures, timeout=timeout, return_when=ALL_COMPLETED
                )

                for fut in done:
                    futures.pop(fut)
                    result.append(fut.result())

            return result
