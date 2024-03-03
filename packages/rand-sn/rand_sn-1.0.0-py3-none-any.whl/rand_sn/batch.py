# standard libraries
import os
from typing import Optional


class Batch:
    """
    Manage batches, which are a sequence of subdirectories named batch00001, batch00002 and so forth.
    """

    number: int or None
    path: str or None
    directory: str or None
    path_directory: str or None
    _prefix: str = 'batch'
    _digits: int = 5

    def __init__(self, path: Optional[str] = None) -> None:
        """
        Initialize FullCycleRandom instance.

        Args:
            path (str): the path where the batch directory will be stored, defaults to the current working directory

        Returns:
            None
        """
        if path is None:
            path = os.getcwd()
        elif not os.path.isdir(path):
            raise ValueError(f"Path {path} is not a directory.")
        self.path = path

        self.number = self._next_number()
        self.directory = f"{self._prefix}{str(self.number).zfill(self._digits)}"
        self.path_directory = os.path.join(self.path, self.directory)
        os.mkdir(self.path_directory)

    def delete(self) -> None:
        """
        Delete the current directory and contents, useful for aborting a batch.

        Returns:
            None
        """
        if self.path_directory is not None:
            os.rmdir(self.path_directory)
            self.number = None
            self.path = None
            self.directory = None
            self.path_directory = None

    def _next_number(self) -> int:
        """
        Return the next batch number, starting at 1.

        Raises:
            ValueError: If the next batch number would be out of range.

        Returns:
            int: Batch number

        """
        if os.path.exists(self.path):
            dirs = os.listdir(self.path)
            numbers = [int(d[self._digits:]) for d in dirs if d.startswith(self._prefix) and d[self._digits:].isdigit()]
            if numbers:
                next_number = max(numbers) + 1
                if len(str(next_number)) > self._digits:
                    raise ValueError(f"Next {self._prefix} number has too many digits")
                else:
                    return max(numbers) + 1
        return 1
