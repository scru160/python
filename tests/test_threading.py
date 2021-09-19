from __future__ import annotations

import queue
import threading
import unittest

from scru160 import scru160f


class TestThreading(unittest.TestCase):
    def test_threading(self) -> None:
        """Generates no IDs sharing same timestamp and counter under multithreading"""

        def producer(q: queue.Queue[str]) -> None:
            for i in range(1000):
                q.put(scru160f())

        q: queue.Queue[str] = queue.Queue()
        for i in range(40):
            threading.Thread(target=producer, args=(q,)).start()

        s = set()
        while not (q.empty() and threading.active_count() < 2):
            ts_and_cnt = q.get()[0:16]
            s.add(ts_and_cnt)

        self.assertEqual(len(s), 1000 * 40)
