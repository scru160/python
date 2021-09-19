import datetime
import math
import typing
import unittest

from scru160 import scru160 as generate


class TestScru160(unittest.TestCase):
    _samples: typing.List[str] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls._samples = [generate() for _ in range(100_000)]

    def test_format(self) -> None:
        """Generates 32-character base32hexupper string"""
        for e in self._samples:
            self.assertEqual(type(e), str)
            self.assertRegex(e, r"^[0-9A-V]{32}$")

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
            ts = int(generate()[0:10], base=32) >> 2
            self.assertLess(abs(now - ts), 16)

    def test_timestamp_and_counter(self) -> None:
        """Encodes unique sortable pair of timestamp and counter"""
        e = self._samples[0]
        prevTs = int(e[0:10], base=32) >> 2
        prevCnt = 0xFFFF & (int(e[9:13], base=32) >> 1)
        for e in self._samples[1:]:
            curTs = int(e[0:10], base=32) >> 2
            curCnt = 0xFFFF & (int(e[9:13], base=32) >> 1)
            self.assertTrue(prevTs < curTs or (prevTs == curTs and prevCnt < curCnt))
            prevTs = curTs
            prevCnt = curCnt

    def test_random_bits(self) -> None:
        """Sets random bits randomly (this may fail at 0.001% probability)"""
        # count '1' in each bit
        bins = [0] * 160
        for e in self._samples:
            for i, b in enumerate(f"{int(e, base=32):160b}"):
                if b == "1":
                    bins[i] += 1

        # test if random bits are set to 1 at ~50% probability
        # set margin based on binom dist 99.999% confidence interval
        n = len(self._samples)
        margin = 4.417173 * math.sqrt((0.5 * 0.5) / n)
        for i, j in enumerate(bins[64:], start=64):
            p = j / n
            self.assertLess(abs(p - 0.5), margin, f"Msb {i}: {p}")
