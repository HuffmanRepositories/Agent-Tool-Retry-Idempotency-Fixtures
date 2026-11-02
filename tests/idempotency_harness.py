"""SQLite-backed synthetic tool-effect/idempotency harness.

Test-only model: effect and idempotency ledger share one SQLite transaction.
This does not prove external provider side effects can be made atomic.
"""
from __future__ import annotations
import hashlib
import json
import sqlite3
from pathlib import Path


class IdempotencyConflict(Exception):
    pass


class TransactionalTool:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS operations (
                scope TEXT NOT NULL, idem_key TEXT NOT NULL, payload_hash TEXT NOT NULL,
                result_json TEXT NOT NULL, PRIMARY KEY(scope, idem_key))""")
            db.execute("""CREATE TABLE IF NOT EXISTS effects (
                effect_id INTEGER PRIMARY KEY AUTOINCREMENT, scope TEXT NOT NULL,
                idem_key TEXT NOT NULL, payload_json TEXT NOT NULL,
                UNIQUE(scope, idem_key))""")

    def _connect(self):
        db = sqlite3.connect(self.db_path, timeout=15, isolation_level=None)
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=FULL")
        return db

    @staticmethod
    def _canonical(payload):
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def call(self, *, scope: str, key: str, payload: dict,
             fail_before_commit: bool = False) -> dict:
        canonical = self._canonical(payload)
        digest = hashlib.sha256(canonical.encode()).hexdigest()
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT payload_hash, result_json FROM operations WHERE scope=? AND idem_key=?",
                             (scope, key)).fetchone()
            if row:
                if row[0] != digest:
                    db.rollback()
                    raise IdempotencyConflict("key reused with different payload")
                result = json.loads(row[1])
                db.commit()
                return result
            # The simulated effect and operation ledger share one DB transaction.
            db.execute("INSERT INTO effects(scope, idem_key, payload_json) VALUES(?,?,?)",
                       (scope, key, canonical))
            effect_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            result = {"status": "completed", "effect_id": effect_id}
            db.execute("INSERT INTO operations(scope, idem_key, payload_hash, result_json) VALUES(?,?,?,?)",
                       (scope, key, digest, json.dumps(result, sort_keys=True)))
            if fail_before_commit:
                db.rollback()
                raise RuntimeError("injected crash before transaction commit")
            db.commit()
            return result

    def effect_count(self, *, scope: str, key: str) -> int:
        with self._connect() as db:
            return db.execute("SELECT COUNT(*) FROM effects WHERE scope=? AND idem_key=?",
                              (scope, key)).fetchone()[0]
