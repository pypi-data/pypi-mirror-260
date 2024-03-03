# *** A way to run these unit tests. ***
# 1. (Open a terminal, alternately known as go to the command line.)
# 2. cd .. (Or, somehow make the project root the current directory.)
# 3. python -m unittest tests/tests

# Standard library imports
import os
from pathlib import Path
import random
import tempfile
import time
import shutil
import unittest

# 3rd party libraries


# Local imports
from src.rand_sn.batch import Batch
from src.rand_sn.config import Config
from src.rand_sn.full_cycle_random import FullCycleRandom
from src.rand_sn.l_f_s_r import LFSR


class TestBatch(unittest.TestCase):
    def setUp(self):
        self.temp_dir: str = tempfile.mkdtemp()

    def test_delete(self):
        batch = Batch(path=self.temp_dir)
        path_directory = batch.path_directory
        self.assertTrue(Path(path_directory).exists())
        batch.delete()
        self.assertIsNone(batch.number)
        self.assertIsNone(batch.directory)
        self.assertIsNone(batch.path_directory)
        self.assertFalse(Path(path_directory).exists())

    def test_one_two_three(self):
        """ Test that the first three batches are created correctly. """
        max_batch = 3
        batches = [Batch(path=self.temp_dir) for _ in range(max_batch)]
        for i, batch in enumerate(batches):
            self.assertEqual(batch.number, i + 1)
            directory = f"batch{str(i + 1).zfill(batch._digits)}"
            self.assertEqual(batch.directory, directory)
            self.assertEqual(batch.path, self.temp_dir)
            self.assertEqual(batch.path_directory, os.path.join(self.temp_dir, directory))
            batch.delete()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir: str = tempfile.mkdtemp()
        self.file = 'rand-sn-config.json'
        self.path_file = os.path.join(self.temp_dir, self.file)

    def test_init_and_reload(self):
        biggest = 10

        # Configure the bare minium and save to disk
        config = Config(path=self.temp_dir)
        config.configure(biggest=biggest)
        self._validate_config(config)
        config.save()
        self.assertTrue(os.path.exists(config.path_file))
        results1 = (config.smallest, config.seed, config.biggest)

        # Reload and double check consistency
        config = Config(path=self.temp_dir)
        config.load()
        config.first = random.randint(1, biggest)    # simulate that a number had be generated
        self._validate_config(config)
        results2 = (config.smallest, config.seed, config.biggest)
        self.assertEqual(results1, results2)

    def test_overflow(self):
        first = 1
        config = Config(path=self.temp_dir)
        config.configure(biggest=10)
        config.seed_cycle(first)        # establish the first
        config.seed_cycle(first + 1)    # different should be permitted
        with self.assertRaises(OverflowError):
            config.seed_cycle(first)  # simulate cycling back to the first

    def _validate_config(self, config: Config):
        self.assertIsInstance(config.smallest, int)
        self.assertIsInstance(config.seed, int)
        self.assertIsInstance(config.biggest, int)
        self.assertGreater(config.smallest,0)
        self.assertLessEqual(config.smallest, config.seed)
        self.assertLessEqual(config.seed, config.biggest)
        if config.first is not None:
            self.assertIsInstance(config.first, int,"should be None or int")
            self.assertLessEqual(config.smallest, config.first)
            self.assertLessEqual(config.first, config.biggest)
        self.assertEqual(config._file, self.file)
        self.assertEqual(config.path_file, self.path_file)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)


class TestLFSR(unittest.TestCase):

    def setUp(self):
        self.lfsr = LFSR()

    def test_init_raises(self):
        with self.assertRaises(ValueError):
            LFSR(bits=0)
        with self.assertRaises(ValueError):
            LFSR(seed=0)

    def test_init_with_seed(self):
        seed = 123
        bits = 10
        lfsr = LFSR(seed=seed, bits=bits)
        self.assertEqual(lfsr._register, seed)
        self.assertEqual(lfsr._bits, bits)
        self.assertIsInstance(lfsr._taps, tuple)
        self.assertIsInstance(lfsr, LFSR)

    def test_init_without_seed(self):
        bits = 2
        lfsr = LFSR(bits=bits)
        self.assertGreater(lfsr._register, 0)
        self.assertEqual(lfsr._bits, bits)
        self.assertIsInstance(lfsr._taps, tuple)
        self.assertIsInstance(lfsr, LFSR)

    def test_next(self):
        lfsr = LFSR()
        bits = lfsr._bits
        register = lfsr._register
        result = next(lfsr)
        self.assertEqual(lfsr._bits, bits)
        self.assertNotEqual(lfsr._register, register)
        self.assertEqual(lfsr._register, result)
        self.assertNotEqual(result, next(lfsr))

    def test_resume_series(self):
        lfsr = LFSR()
        result_a = next(lfsr)
        result_b_1 = next(lfsr)
        self.assertNotEqual(result_a, result_b_1)

        lfsr = LFSR(seed=result_a)
        result_b_2 = next(lfsr)
        self.assertEqual(result_b_1, result_b_2)

    def test_series_lengths(self):
        """ all possible numbers should be generated before repeating """
        start_time = time.time()
        timeout = 5
        for bits in LFSR._optimal_taps.keys():

            if time.time() - start_time > timeout:  # Check if 5 seconds have passed
                print(f"Incomplete; breaking at {bits} bits, because of a {timeout} second timeout.")
                break  # Break out of the loop if more than 5 seconds have passed

            unique_values = 2 ** bits - 1  # zero is not permitted
            generated = set()
            lfsr = LFSR(bits=bits)
            for number in lfsr:
                if number not in generated:
                    self.assertGreaterEqual(number, 1)
                    self.assertGreaterEqual(bits, number.bit_length())
                    generated.add(number)
                else:
                    self.assertEqual(unique_values, len(generated), f"A {bits} bit series should be {unique_values} long, not {len(generated)}.")
                    break

    def test_for_missing_taps(self):
        """ The keys for the taps should start at 2 and increment. """
        last = 1
        for key in LFSR._optimal_taps.keys():
            self.assertEqual(last + 1, key)
            last = key


class TestFullCycleRandom(unittest.TestCase):

    def test_init_raises(self):
        with self.assertRaises(ValueError):
            FullCycleRandom(min_int=-1, max_int=100)
        with self.assertRaises(ValueError):
            FullCycleRandom(min_int=101, max_int=100)
        with self.assertRaises(ValueError):
            FullCycleRandom(seed=1, min_int=2, max_int=3)
        with self.assertRaises(ValueError):
            FullCycleRandom(seed=10, min_int=20, max_int=30)

    def test_init_success(self):
        min_int = 500
        max_int = 1000
        for seed in (None, 750):
            fcr = FullCycleRandom(seed=seed, min_int=min_int, max_int=max_int)
            self.assertEqual(fcr._min_int, min_int)
            self.assertEqual(fcr._max_int, max_int)
            self.assertIsInstance(fcr._lfsr, LFSR)
            self.assertIsInstance(fcr, FullCycleRandom)

    def test_next(self):
        fsr = FullCycleRandom()
        min_int = fsr._min_int
        max_int = fsr._max_int
        result = next(fsr)
        self.assertEqual(fsr._min_int, min_int)
        self.assertEqual(fsr._max_int, max_int)
        self.assertLessEqual(min_int, result)
        self.assertLessEqual(result, max_int)
        self.assertNotEqual(result, next(fsr))

    def test_resume_series(self):
        fcr = FullCycleRandom()
        result_a = next(fcr)
        result_b_1 = next(fcr)
        self.assertNotEqual(result_a, result_b_1)

        fcr = FullCycleRandom(seed=result_a)
        result_b_2 = next(fcr)
        self.assertEqual(result_b_1, result_b_2)

    def test_series_length(self):
        """ All possible numbers should be generated before repeating """
        for (min_int, max_int) in ((1, 1),  # smallest possible
                                   (1, 6),  # use all but one bit of 3-bit shift register
                                   (1, 7),  # use all 3-bits
                                   (1, 8),  # barely require 4-bits
                                   (50, 99999),     # a wide range with a practical run-time
                                   (99999999999999999999999998, 99999999999999999999999999),    # big shift, use 2-bits
                                   ):
            unique_values = max_int - min_int + 1
            fcr = FullCycleRandom(min_int=min_int, max_int=max_int)
            generated = set()
            for number in fcr:
                if number not in generated:
                    self.assertGreaterEqual(number, min_int)
                    self.assertLessEqual(number, max_int)
                    generated.add(number)
                else:
                    self.assertEqual(unique_values, len(generated))
                    break   # series complete


if __name__ == "__main__":
    unittest.main()
