from abc import ABCMeta, abstractmethod
from typing import Callable
import logging


logger = logging.getLogger('root')


class CommandFactory:
    """ The factory class for creating commands"""

    registry = {}
    """ Internal registry for available commands """

    @classmethod
    def register(cls, name: str) -> Callable:
        """ Class method to register Command class to the internal registry.
        Args:
            name (str): The name of the command.
        Returns:
            The Command class itself.
        """

        def inner_wrapper(wrapped_class: CommandBase) -> Callable:
            if name in cls.registry:
                logger.warning('Command %s already exists.', name)
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def create_command(cls, name: str, **kwargs) -> 'CommandBase':
        if name not in cls.registry:
            return None

        cmd_class = cls.registry[name]
        command = cmd_class(**kwargs)
        return command

    @classmethod
    def is_command_registered(cls, cmd):
        if cmd not in cls.registry:
            return False
        else:
            return True

    @classmethod
    def get_registered_commands(cls):
        return cls.registry.keys()


class CommandBase(metaclass=ABCMeta):
    """ Base class for a Command """

    @abstractmethod
    def execute(self, args):
        pass

    @abstractmethod
    def get_help(self):
        pass
