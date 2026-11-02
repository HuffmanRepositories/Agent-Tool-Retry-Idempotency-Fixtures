# Review checklist

- [ ] Fixture is synthetic and contains no live credentials or sensitive data.
- [ ] Scenario and assumptions are explicit.
- [ ] Logical operation identity is distinguished from attempt identity.
- [ ] Request payload/key consistency is addressed where relevant.
- [ ] Effect status is not inferred solely from response delivery.
- [ ] Unknown outcome is preserved when evidence is insufficient.
- [ ] Retry safety is grounded in operation semantics, not a blanket rule.
- [ ] Concurrent and late-arriving events are considered.
- [ ] Expected behavior is descriptive, not presented as universal protocol law.
- [ ] Fixture is listed in `docs/fixture-status.md`.
- [ ] Validator and unit tests pass.
