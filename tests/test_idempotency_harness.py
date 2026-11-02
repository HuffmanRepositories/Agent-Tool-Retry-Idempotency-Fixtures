import tempfile
import threading
import unittest
from pathlib import Path

from idempotency_harness import IdempotencyConflict, TransactionalTool


class TransactionalIdempotencyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "tool.sqlite"
        self.tool = TransactionalTool(self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def test_response_lost_after_commit_replay_after_restart(self):
        first = self.tool.call(scope="acct:1", key="k", payload={"amount": 4})
        restarted = TransactionalTool(self.db)
        replay = restarted.call(scope="acct:1", key="k", payload={"amount": 4})
        self.assertEqual(first, replay)
        self.assertEqual(restarted.effect_count(scope="acct:1", key="k"), 1)

    def test_same_key_different_payload_conflicts(self):
        self.tool.call(scope="acct:1", key="k", payload={"amount": 4})
        with self.assertRaises(IdempotencyConflict):
            self.tool.call(scope="acct:1", key="k", payload={"amount": 5})
        self.assertEqual(self.tool.effect_count(scope="acct:1", key="k"), 1)

    def test_concurrent_duplicate_calls_commit_one_effect(self):
        barrier = threading.Barrier(12)
        results, errors = [], []
        def worker():
            try:
                barrier.wait(timeout=5)
                results.append(self.tool.call(scope="acct:1", key="shared",
                                             payload={"op": "charge", "amount": 8}))
            except Exception as exc:
                errors.append(exc)
        threads = [threading.Thread(target=worker) for _ in range(12)]
        for thread in threads: thread.start()
        for thread in threads: thread.join(timeout=10)
        self.assertFalse(any(thread.is_alive() for thread in threads), "thread deadlock")
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 12)
        self.assertTrue(all(result == results[0] for result in results))
        self.assertEqual(self.tool.effect_count(scope="acct:1", key="shared"), 1)

    def test_crash_before_commit_rolls_back_effect_and_ledger(self):
        with self.assertRaisesRegex(RuntimeError, "injected crash"):
            self.tool.call(scope="acct:1", key="crash", payload={"x": 1},
                           fail_before_commit=True)
        self.assertEqual(self.tool.effect_count(scope="acct:1", key="crash"), 0)
        result = self.tool.call(scope="acct:1", key="crash", payload={"x": 1})
        self.assertEqual(result["status"], "completed")
        self.assertEqual(self.tool.effect_count(scope="acct:1", key="crash"), 1)

    def test_key_scope_isolation(self):
        a = self.tool.call(scope="acct:A", key="same", payload={"x": 1})
        b = self.tool.call(scope="acct:B", key="same", payload={"x": 2})
        self.assertNotEqual(a["effect_id"], b["effect_id"])
        self.assertEqual(self.tool.effect_count(scope="acct:A", key="same"), 1)
        self.assertEqual(self.tool.effect_count(scope="acct:B", key="same"), 1)


if __name__ == "__main__":
    unittest.main()
