# standard libraries
import random
from typing import Dict, Optional, Tuple


class LFSR:
    """
    Linear Feedback Shift Register (LFSR) class.
    """

    _optimal_taps: Dict[int, Tuple[int]] = {
        2: (2, 1),
        3: (3, 2),
        4: (4, 3),
        5: (5, 3),
        6: (6, 5),
        7: (7, 6),
        8: (8, 6, 5, 4),
        9: (9, 5),
        10: (10, 7),
        11: (11, 9),
        12: (12, 6, 4, 1),
        13: (13, 4, 3, 1),
        14: (14, 5, 3, 1),
        15: (15, 14),
        16: (16, 15, 13, 4),
        17: (17, 14),
        18: (18, 11),
        19: (19, 6, 2, 1),
        20: (20, 17),
        21: (21, 19),
        22: (22, 1),
        23: (23, 18),
        24: (24, 23, 22, 17),
        25: (25, 22),
        26: (26, 6, 2, 1),
        27: (27, 5, 2, 1),
        28: (28, 3),
        29: (29, 27),
        30: (30, 6, 4, 1),
        31: (31, 28),
        32: (31, 30, 29, 28, 26, 25, 24, 22, 21, 19, 18, 17, 14, 13, 12, 10, 8, 7, 5, 3, 2, 1),
        33: (33, 20),
        34: (34, 27),
        35: (35, 33),
        36: (36, 25),
        37: (37, 5, 4, 3, 2, 1),
        38: (38, 6, 5, 1),
        39: (39, 4),
        40: (40, 21),
        41: (41, 3),
        42: (42, 41, 20, 19),
        43: (43, 6, 4, 3),
        44: (44, 43, 18, 17),
        45: (45, 4, 3, 1),
        46: (46, 45, 26, 25),
        47: (47, 5),
        48: (48, 29),
        49: (49, 9),
        50: (50, 49, 24, 23),
        51: (51, 6, 3, 1),
        52: (52, 3),
        53: (53, 6, 2, 1),
        54: (54, 7, 6, 1),
        55: (55, 7),
        56: (56, 7, 4, 2),
        57: (57, 7, 4, 3),
        58: (58, 19),
        59: (59, 6, 5, 1),
        60: (60, 1),
        61: (61, 6, 5, 1),
        62: (62, 29, 27, 1),
        63: (63, 1),
        64: (63, 61, 60, 59),
        # Add more lengths and their optimal taps as needed,
        # optimal taps produce the longest possible sequence.
    }

    def __init__(self, seed: Optional[int] = None, bits: int = 8):
        """
        Initialize LFSR instance.

        :param seed: Start or resume the sequence with a known integer, or None for a random start, defaults to None.
        :param bits: The number of bits in the shift register.
        :return: Returns nothing.
        """

        # determine the number of bits that will be in the shift register
        if not isinstance(bits, int):
            raise TypeError('The bits parameter must be an integer.')
        elif bits not in self._optimal_taps:
            available_keys = list(self._optimal_taps.keys())
            raise ValueError(f"Invalid bits. Please choose from the following integers: {available_keys}")
        else:
            self._bits = bits

        # determine what bits will be tapped and then adjust for how Python indexes bits
        self._taps = tuple([bits - tap for tap in self._optimal_taps[bits]])

        # determine the shift register's initial value, the proper term for this is the seed
        max_register = self._max_register(bits)
        if seed is None:
            self._register = random.randint(1, max_register)
        elif not isinstance(seed, int):
            raise ValueError("The seed must be an integer or None.")
        elif not (1 <= seed <= max_register):
            raise ValueError(f"The seed must be from 1 to {max_register}.")
        else:
            self._register = seed

    @staticmethod
    def _max_register(n_bits: int) -> int:
        return 2 ** n_bits - 1

    def __iter__(self):
        """
        Return the iterator object itself. This is required for the object
        to be used in for loops and other places where an iterable is expected.

        Returns:
            self: The class instance.
        """
        return self

    def __next__(self) -> int:
        """
        Advance the register by one step in the series.

                1 2 3 4 5 6 7 8 (bits == 8)
               ┌─┬─┬─┬─┬─┬─┬─┬─┐
            ┌─→│0│1│0│1│0│0│1│1├─→
            │  └─┴─┴─┴┬┴┬┴─┴┬┴─┘
            └──────XOR┘ │   │
                    └──XOR──┘ (taps == 7, 5, 4)

        Returns:
            int: The next register in the sequence.
        """
        tap_bits = 0
        for tap in self._taps:
            tap_bits = tap_bits ^ (self._register >> tap) & 1
        bit = tap_bits

        self._register = (self._register >> 1) | (bit << (self._bits - 1))

        return self._register
