"""Verification must bound page resources and clean up unfinished checks on failure."""
import asyncio
import unittest
from tools.check_topics import bounded_checks

class BoundedChecksTests(unittest.IsolatedAsyncioTestCase):
    async def test_limit_and_complete_exactly_once(self):
        active=0;peak=0;seen=[]
        async def worker(item):
            nonlocal active,peak
            active+=1;peak=max(active,peak)
            try:await asyncio.sleep(.001);seen.append(item);return item*2
            finally:active-=1
        self.assertEqual(await bounded_checks(range(9),worker,2),[x*2 for x in range(9)])
        self.assertEqual(sorted(seen),list(range(9)));self.assertEqual(peak,2);self.assertEqual(active,0)

    async def test_failure_cancels_other_page_work(self):
        active=set()
        async def worker(item):
            active.add(item)
            try:
                if item==0:await asyncio.sleep(.001);raise ValueError('Required page failed')
                await asyncio.sleep(60)
            finally:active.remove(item)
        with self.assertRaisesRegex(ValueError,'Required page failed'):await bounded_checks(range(4),worker,2)
        self.assertEqual(active,set())
