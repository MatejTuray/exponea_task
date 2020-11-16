import utils.enums as en

from task_runners.abstract_runners import AbstractRequestRunnerCreator
from task_runners.runner import AllRunner, FirstRunner, SmartRunner


class ExponeaRequestRunnerCreator(AbstractRequestRunnerCreator):
    def __init__(self):
        self.runners = {
            en.TaskTypes.ALL_SUCCESSFUL.name: AllRunner,
            en.TaskTypes.FIRST_SUCCESSFUL.name: FirstRunner,
            en.TaskTypes.WITHIN_TIMEOUT.name: AllRunner,
            en.TaskTypes.SMART.name: SmartRunner,
        }

    def create_runner(self, runner_type):
        return self.runners[runner_type]()
