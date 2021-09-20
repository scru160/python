import secrets
import unittest

from scru160 import _base32hex160


class TestBase32hex160(unittest.TestCase):
    def test_testbase32hex160(self) -> None:
        """Private: _base32hex160() encodes 20-byte sequence into base32hex."""
        for _ in range(1000):
            n = secrets.randbits(160)
            self.assertEqual(int(_base32hex160(n.to_bytes(20, "big")), 32), n)
