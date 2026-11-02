# Contributing

Contributions should improve clarity, reproducibility, and neutrality.

1. Keep fixtures synthetic and deterministic.
2. Separate observed facts from expected behavior and assumptions.
3. Avoid claiming universal semantics where tool/protocol contracts differ.
4. Document whether a case depends on durable storage, key scope, or retention.
5. Run:
   ```bash
   python scripts/validate_fixtures.py
   python -m unittest discover -s tests
   ```
6. Update `docs/fixture-status.md` and explain any changed expected outcomes.

Do not submit credentials, personal data, live endpoints, or instructions for harmful side effects. A fixture passing the structural validator is not evidence of implementation correctness.
