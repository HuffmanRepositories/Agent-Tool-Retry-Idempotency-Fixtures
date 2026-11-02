# Agent Tool Retry & Idempotency Fixtures

[Start here](START-HERE.md) · [AI agent guidance](AGENTS.md)


An implementation-neutral, synthetic fixture corpus for reviewing retry and idempotency behavior in agent tool execution.

> Status: draft fixtures, not a standard, certification, or conformance suite.

## Why this exists

Agent tool calls can have side effects. A timeout or lost response does not necessarily mean the effect did not happen. Retrying blindly can duplicate an operation; refusing to retry can leave work incomplete. This corpus captures ambiguous outcomes and reviewable expected behavior without prescribing a runtime.

## Scope

**In scope**
- Synthetic request/effect/response sequences
- Idempotency-key and payload consistency
- Duplicate and concurrent attempts
- Partial effects, cancellation, restart, reconciliation
- Distinguishing retryable errors from permanent errors and unknown outcomes

**Out of scope**
- SDKs, middleware, retry engines, durable-execution systems, or services
- Protocol definitions or a universal idempotency-key format
- Claims of exactly-once execution
- Real-world tool calls, production data, security exploits, or certification

## Fixture status

All included fixtures are **synthetic draft examples**. They are not validated against implementations or external systems. See [fixture-status](docs/fixture-status.md).

## Validate locally

Requires Python 3.10+; the validator uses only the standard library.

```bash
python scripts/validate_fixtures.py
python -m unittest discover -s tests
```

## Design principle

An idempotency key is not magic. A correct retry policy depends on the operation's semantics, key scope and retention, request identity, durable effect recording, and how the caller handles an unknown outcome. “Exactly once” should not be inferred from retry suppression alone.

## References

- [MCP issue: mutating tool call and lost response](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/3394)
- [LangGraph issue: durable idempotency and retry middleware](https://github.com/langchain-ai/langgraph/issues/8464)
- [Microsoft MCP reliability sidecars](https://github.com/microsoft/mcp-for-beginners/blob/main/08-BestPractices/reliability-sidecars/README.md)
- [Golem durable execution](https://github.com/golemcloud/golem/blob/main/docs/src/content/next/concepts/durable-execution.mdx)
- [ADK Rust tool effects](https://github.com/zavora-ai/adk-rust/blob/main/docs/official_docs/tools/tool-effects.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), [fixture format](docs/fixture-format.md), and [review checklist](docs/review-checklist.md).
