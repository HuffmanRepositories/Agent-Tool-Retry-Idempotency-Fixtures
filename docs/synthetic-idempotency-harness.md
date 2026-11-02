# P12 Synthetic Durable Idempotency Harness

**Status:** experimental synthetic component harness; not a runtime, conformance suite, or exactly-once guarantee.

## What this harness tests

The Python harness in `tests/idempotency_harness.py` uses SQLite to model an operation ledger and a side-effect record committed in the **same local transaction**. Tests exercise:

1. Response lost after transaction commit; replay after constructing a fresh service instance.
2. Same idempotency key with a changed payload produces a conflict and no duplicate effect.
3. Twelve concurrent same-key requests across threads return the same result and create one modeled effect.
4. Injected crash before transaction commit rolls back both effect and ledger, after which a retry can execute.
5. Same key in different scopes does not collide.

Run:

```bash
python -m unittest discover -s tests
```

## Boundaries and non-claims

This SQLite arrangement is a controlled **single-database atomicity demonstration**. It is not proof that an external provider's effect and our ledger can be committed atomically. If the provider is outside the transaction boundary, the system needs provider idempotency, durable reconciliation, an outbox/inbox pattern where applicable, or an explicit `unknown` outcome and domain-specific recovery. It must not blindly repeat an uncertain side effect.

It does not test:
- real external services or API calls;
- multi-host/distributed deployment, network partition, failover or clock drift;
- exactly-once effects;
- key expiry, eviction, retention, tenant identity authentication or authorization;
- provider-specific reconciliation, refunds or partial side effects;
- load/performance or production durability guarantees.

The harness uses a synthetic local SQLite database and fake effect table only. No real money, credentials, user data, or remote services are involved.

## Follow-up design decisions required

Before adopting a production protocol, define:
- key namespace (tenant/account, tool, operation, API version);
- canonical payload hashing and treatment of semantically equivalent JSON;
- retention/expiry and behavior after key expiry;
- what constitutes final, retryable, permanent, partial, and unknown outcome;
- provider-side dedupe and reconciliation support;
- transaction boundary, ledger durability and disaster recovery;
- authorization checks on both initial request and replay (avoid leaking cached result across actors);
- replay response semantics and audit trace IDs.
