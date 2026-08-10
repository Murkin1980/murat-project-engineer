# Acceptance evidence

| Criterion | Deterministic evidence | Result |
|---|---|---|
| Inside values remain unchanged | `test_value_inside_range` | PASS |
| Values below minimum clamp to minimum | `test_value_below_range` | PASS |
| Values above maximum clamp to maximum | `test_value_above_range` | PASS |
| Invalid range raises `ValueError` | `test_invalid_range` | PASS |

All criteria map to passing unit tests in `test-results.txt`.
