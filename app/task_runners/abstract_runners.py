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


class AbstractRequestRunnerCreator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_runner(self, type):
        raise NotImplementedError
