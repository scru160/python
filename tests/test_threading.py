from __future__ import annotations

import queue
import threading
import unittest

from scru160 import scru160, scru160f


class TestThreading(unittest.TestCase):
    def test_threading(self) -> None:
        """Generates no IDs sharing same timestamp and counter under multithreading"""

        def producer(q: queue.Queue[str]) -> None:
            for i in range(10000):
                q.put(scru160())
                q.put(scru160f())

        q: queue.Queue[str] = queue.Queue()
        for i in range(4):
            threading.Thread(target=producer, args=(q,)).start()

        s = set()
        while not (q.empty() and threading.active_count() < 2):
            e = q.get()
            ts_and_cnt = int(e[0:13], 32) >> 1 if len(e) == 32 else int(e[0:16], 16)
            s.add(ts_and_cnt)

        self.assertEqual(len(s), 4 * 10000 * 2)
