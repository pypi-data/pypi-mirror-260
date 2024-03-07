import os

from typing import Optional, Union, List
from friday.utils.schema import EnvState


class Env:
    """
    A base class for environment configurations in action-based systems.

    This class provides foundational attributes and methods for managing environments,
    including timeouts, working directories, and environmental states. It is designed
    to be extended by subclasses that implement specific environment behaviors.
    """

    def __init__(self) -> None:
        """
        Initializes the environment with default settings.

        Sets up the working directory, applying a default timeout and preparing the
        environment state. If the working directory does not exist, it is created.
        """
        self._name: str = self.__class__.__name__
        self.timeout: int = 300
        self.working_dir = os.path.abspath(os.path.join(__file__, "..", "..", "..", "working_dir"))
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)

        self.env_state: Union[EnvState, None] = None

    def list_working_dir(self):
        """
        Lists the contents of the working directory in a detailed format.

        Returns a string representation similar to the output of the 'ls' command in Linux,
        including file/directory names, sizes, and types.

        Returns:
            str: Detailed listings of the working directory's contents, or an error message if the directory does not exist.
        """
        directory = self.working_dir
        # Check if the directory exists
        if not os.path.exists(directory):
            return f"Directory '{directory}' does not exist."

        # List files and directories
        files_and_dirs = os.listdir(directory)

        # Create a list to store the details
        details = []

        for name in files_and_dirs:
            # Get the full path
            full_path = os.path.join(directory, name)

            # Get file or directory size
            size = os.path.getsize(full_path)

            # Check if it's a file or directory
            if os.path.isdir(full_path):
                type = 'Directory'
            else:
                type = 'File'

            details.append(f"{name}\t {size} bytes\t {type}")

        return "\n".join(details)
        
    def step(self, _command) -> EnvState:
        """
        Executes a command within the environment.

        This method is intended to be implemented by subclasses, defining how commands
        are processed and their effects on the environment state.

        Args:
            _command: The command to be executed.

        Raises:
            NotImplementedError: Indicates that the subclass must implement this method.

        Returns:
            EnvState: The state of the environment after executing the command.
        """
        raise NotImplementedError

    def reset(self):
        """
        Resets the environment to its initial state.

        This method is intended to be implemented by subclasses, defining the specific
        actions required to reset the environment.

        Raises:
            NotImplementedError: Indicates that the subclass must implement this method.
        """
        raise NotImplementedError
    
    @property
    def name(self):
        """
        The name of the environment.

        Returns:
            str: The name of the environment, typically set to the class name unless overridden in a subclass.
        """
        return self._name

    def __repr__(self):
        """
        Provides a string representation of the environment.

        Returns:
            str: A representation of the environment, including its name.
        """
        return f'{self.name}'

    def __str__(self):
        """
        Returns the string representation of the environment, mirroring `__repr__`.

        Returns:
            str: A string representation of the environment.
        """
        return self.__repr__()


if __name__ == '__main__':
    env = Env()
    env.env_state = EnvState()
    # result = env.observe()
