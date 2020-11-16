import utils.enums as en
from task_runners.runner import (
    AllRunner,
    FirstRunner,
    SmartRunner,
)
from interfaces.runnerInterface import AbstractRequestRunnerFactory

import abc


class AbstractRunner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def push_task(self):
        """
        docstring
        """
        raise NotImplementedError

    @abc.abstractmethod
    def schedule_tasks(self):
        """
        docstring
        """
        raise NotImplementedError


class AbstractRequestRunnerFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_runner(self, type):
        raise NotImplementedError


class ExponeaRequestRunnerFactory(AbstractRequestRunnerFactory):
    def __init__(self):
        self.runners = {
            en.TaskTypes.ALL_SUCCESSFUL.name: AllRunner,
            en.TaskTypes.FIRST_SUCCESSFUL.name: FirstRunner,
            en.TaskTypes.WITHIN_TIMEOUT.name: AllRunner,
            en.TaskTypes.SMART.name: SmartRunner,
        }

    def create_runner(self, runner_type):
        return self.runners[runner_type]()
