# Fixture status

All entries are **synthetic draft fixtures**. Structural validation does not mean these cases have been tested against any tool implementation or protocol.

| ID | Scenario | Status |
|---|---|---|
| retry-001 | Effect committed, response lost | draft |
| retry-002 | Timeout before commit | draft |
| retry-003 | Same key, changed payload | draft |
| retry-004 | Distinct operation uses new key | draft |
| retry-005 | Concurrent duplicate requests | draft |
| retry-006 | Partial effect and reconciliation | draft |
| retry-007 | Late result after cancellation | draft |
| retry-008 | Restart between claim and result record | draft |
| retry-009 | Retryable vs permanent error | draft |
| retry-010 | Key expiry boundary | draft |
| retry-011 | Read-only vs mutating retry | draft |
| retry-012 | Retry exhaustion with unknown outcome | draft |

No certification, runtime conformance, interoperability, or exactly-once guarantee is implied.
