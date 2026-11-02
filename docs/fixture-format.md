# Fixture format

Each fixture is a UTF-8 JSON object with these required fields:

| Field | Meaning |
|---|---|
| `id` | Stable, unique identifier |
| `title` | Short human-readable title |
| `category` | Retry/idempotency scenario class |
| `status` | Currently `draft` |
| `description` | Scenario setup |
| `assumptions` | Explicit environment/operation assumptions |
| `events` | Ordered sequence of synthetic events |
| `expected` | Expected interpretation or handling |
| `failure_modes` | Potential incorrect behavior |
| `notes` | Caveats or boundaries |

Events are intentionally generic. They do not define a wire protocol, transport API, or mandated retry policy.

## Outcome vocabulary

- **completed**: effect is known to have committed
- **not_committed**: evidence supports no effect having committed
- **unknown**: effect status cannot be determined from available evidence
- **conflict**: same logical key used with incompatible operation identity/payload
- **reconcile**: consult durable operation state or a domain-specific recovery path before repeating a side effect

Avoid converting `unknown` into `not_committed` merely because a response timed out.
