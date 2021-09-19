import datetime
import math
import typing
import unittest

from scru160 import scru160f as generate


class TestScru160f(unittest.TestCase):
    _samples: typing.List[str] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls._samples = [generate() for _ in range(100_000)]

    def test_format(self) -> None:
        """Generates 40-character hexadecimal string"""
        for e in self._samples:
            self.assertEqual(type(e), str)
            self.assertRegex(e, r"^[0-9a-f]{40}$")

    def test_uniqueness(self) -> None:
        """Generates 100k identifiers without collision"""
        self.assertEqual(len(set(self._samples)), len(self._samples))

    def test_order(self) -> None:
        """Generates sortable string representation by creation time"""
        sorted_copy = sorted(self._samples)
        for i, e in enumerate(self._samples):
            self.assertEqual(e, sorted_copy[i])

    def test_timestamp(self) -> None:
        """Encodes up-to-date unix timestamp"""
        for i in range(10_000):
            now = int(datetime.datetime.now().timestamp() * 1000)
            ts = int(generate()[0:12], base=16)
            self.assertLess(abs(now - ts), 16)

    def test_timestamp_and_counter(self) -> None:
        """Encodes unique sortable pair of timestamp and counter"""
        e = self._samples[0]
        prevTs = int(e[0:12], base=16)
        prevCnt = int(e[12:16], base=16)
        for e in self._samples[1:]:
            curTs = int(e[0:12], base=16)
            curCnt = int(e[12:16], base=16)
            self.assertTrue(prevTs < curTs or (prevTs == curTs and prevCnt < curCnt))
            prevTs = curTs
            prevCnt = curCnt

    def test_random_bits(self) -> None:
        """Sets random bits randomly (this may fail at 0.001% probability)"""
        # count '1' in each bit
        bins = [0] * 160
        for e in self._samples:
            for i, b in enumerate(f"{int(e, base=16):160b}"):
                if b == "1":
                    bins[i] += 1

        # test if random bits are set to 1 at ~50% probability
        # set margin based on binom dist 99.999% confidence interval
        n = len(self._samples)
        margin = 4.417173 * math.sqrt((0.5 * 0.5) / n)
        for i, j in enumerate(bins[64:], start=64):
            p = j / n
            self.assertLess(abs(p - 0.5), margin, f"Msb {i}: {p}")
