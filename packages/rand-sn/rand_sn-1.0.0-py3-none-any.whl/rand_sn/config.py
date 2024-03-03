# standard libraries
import json
import random
import os
from typing import Optional


class Config:
    smallest: int                   # the smallest number permitted
    seed: int                       # the last number generated, used to determine the next
    biggest: int                    # the largest number permitted
    first: Optional[int] = None     # the first number generated, stop if we reach it again
    prefix: Optional[str]           # a URL stub placed before the number in the QR code
    _file: str                      # the configuration's file name
    path_file: Optional[str] = None     # the path to the configuration file
    _extension: str = '.json'       # the mandatory file extension

    def __init__(self,
                 path: Optional[str] = None,
                 config_filename: Optional[str] = None,
                 ):
        """
        Initialize Config instance.

        Args:
            path (str): the path where the config file is or will be stored, defaults to the current working directory
            config_filename (str): The file name with or without extension, default 'rand-sn-config'

        Returns:
            None
        """
        # path
        if path is None:
            path = os.getcwd()
        elif not os.path.isdir(path):
            raise ValueError(f"Path {path} is not a directory.")

        # filename, if need be, add the extension
        if config_filename is None:
            self._file = 'rand-sn-config'
        else:
            self._file = config_filename
        if not self._file.endswith(self._extension):
            self._file += self._extension

        # both
        self.path_file = os.path.join(path, self._file)

    def configure(self, biggest: int, smallest: Optional[int] = 1, prefix: Optional[str] = None):
        """
        Configure when there is nothing to load from disk.

        Args:
            smallest (int): the smallest integer that the serial number can be
            biggest (int): the biggest integer that the serial number can be
            prefix (str): The prefix to use in QR code generation, example 'https://yourdomain.com/c/'

        Returns:
            None
        """
        self.prefix = prefix
        self.smallest = smallest
        self.biggest = biggest
        self.seed = self.smallest    # redo after validation, prevent type errors on the random call
        self._validate()
        self.seed = random.randint(self.smallest, self.biggest)

    def seed_cycle(self, number: int):
        """
        Update the seed and check if the cycle is about to repeat.

        Args:
            number (int): the current number in the sequence

        Returns:
            None or raises OverflowError
        """
        if self.first is None:
            self.first = number
        elif self.first == number:
            raise OverflowError
        self.seed = number

    def save(self) -> None:
        """
        Save configuration to file.
        :return: None
        """
        self._validate()
        warning = "Preserve the seed! Back-up this file and don't delete it."
        config_dict = {'*warning*': warning, 'first': self.first, 'smallest': self.smallest, 'seed': self.seed, 'biggest': self.biggest, 'prefix': self.prefix}
        with open(self.path_file, 'w') as f:
            json.dump(config_dict, f, indent=4)

    def load(self) -> None:
        """
        Load configuration from file.
        :return: None.
        """
        with open(self.path_file, 'r') as f:
            config_dict = json.load(f)
            config_dict.pop('*warning*')
            for key, value in config_dict.items():
                setattr(self, key, value)
            self._validate()

    def _validate(self) -> None:
        """
        Validate all the class variables.
        :return: None.
        """
        for (variable, value) in (('smallest', self.smallest), ('seed', self.seed), ('biggest', self.biggest)):
            if not isinstance(value, int):
                raise TypeError(f"{variable} is not an integer")
        if not (0 < self.smallest <= self.seed <= self.biggest):
            raise ValueError("Range error, 0 < smallest <= seed <= biggest is required.")

        if self.prefix is not None and not isinstance(self.prefix, str):
            raise TypeError("Prefix must be None or a string.")

        if self.first is not None:
            if not isinstance(self.first, int):
                raise TypeError("First must be None or an int.")
            elif not (self.smallest <= self.first <= self.biggest):
                raise ValueError("Range error, smallest <= first <= biggest is required.")

        if not isinstance(self._file, str):
            raise TypeError("_file must be a string.")
        if not self._file.endswith(self._extension):
            raise ValueError(f"_file must end with {self._extension}.")
        if self._file == self._extension:
            raise ValueError(f"_file must have something before {self._extension}.")

        if not isinstance(self.path_file, str):
            raise TypeError("_path_file must be a string.")
        if not self.path_file.endswith(self._extension):
            raise ValueError(f"_path_file must end with {self._extension}.")
        if len(self.path_file) <= len(self._file):
            raise ValueError(f"the path is missing from _path_file {self.path_file}.")
