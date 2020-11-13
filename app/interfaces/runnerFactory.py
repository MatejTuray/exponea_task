import itertools
import abc
from app.interfaces.taskInterface import TaskTypes
from app.task_runners.runner import AllRunner, FirstRunner, TimeoutRunner, SmartRunner

class AbstractRunner(abc.ABCMeta):
    @abc.abstractclassmethod
    def push_task(self, parameter_list):
        """
        docstring
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def schedule_tasks(self, parameter_list):
        """
        docstring
        """
        raise NotImplementedError


class AbstractRequestRunnerFactory(abc.ABCMeta):
    @abc.abstractmethod
    def create_runner(self, type):
        raise NotImplementedError
    

class ExponeaRequestRunnerFactory(AbstractRequestRunnerFactory):
    def __init__(self):
        self.runners = {
            TaskTypes.ALL_SUCCESSFUL.name: AllRunner,
            TaskTypes.FIRST_SUCCESSFUL.name: FirstRunner,
            TaskTypes.WITHIN_TIMEOUT.name: TimeoutRunner,
            TaskTypes.SMART.name: SmartRunner,
        }

    def create_runner(self, runner_type):
        return self.runners[runner_type]()