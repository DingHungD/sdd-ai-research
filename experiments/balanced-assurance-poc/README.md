# Balanced Assurance PoC

This experiment implements the first recommended SDD stack:

`OpenSpec + OpenLore + cc-sdd + OPA/Rego + Conftest`

It assumes an SDD document already exists. The PoC focuses on the reliable
handoff from that document to a merge gate. It is an executable integration
contract, not a vendored copy of the five upstream tools.

## Tool Boundaries

| Layer | PoC artifact | Replace with real tool output |
| --- | --- | --- |
| SDD input | `sdd/requirements.md` | Existing requirement document |
| OpenSpec | `openspec/*.json` | Approved requirements and change proposal |
| OpenLore | `openlore/*.json` | Repository context graph and drift report |
| cc-sdd | `cc-sdd/*.json` | Task execution plan and evidence bundle |
| Security controls | `policy/security-controls.yaml` | JSON-compatible YAML control registry |
| OPA/Rego | `policy/main.rego` | Versioned organization policy pack |
| Conftest | `artifacts/gate-input.json` | PR, CI and deploy policy test input |

The Python adapter builds the structured Conftest input and runs equivalent
local checks. This makes the experiment runnable before `conftest` is
installed. CI installs Conftest and executes the real Rego policy.

## Run

```text
python scripts/run_balanced_assurance_poc.py --skip-conftest
python scripts/run_balanced_assurance_poc.py --require-conftest
```

The first command runs anywhere with Python. The second requires Conftest and
is the command used by CI.

To demonstrate a blocked merge:

```text
python scripts/run_balanced_assurance_poc.py --skip-conftest \
  --overrides experiments/balanced-assurance-poc/fixtures/failing-overrides.json \
  --output-dir experiments/balanced-assurance-poc/artifacts/failing
```

The failing fixture introduces a stale brownfield node and a failed test.

The observed results and current limitations are recorded in
[`RESULTS.md`](RESULTS.md).

## Acceptance Criteria

- Every requirement maps to approved proposal, task, code path, test and review evidence.
- Brownfield drift has a reviewed impact analysis and no stale or orphan nodes.
- Security controls are versioned and marked as enforced.
- The Python verifier passes locally.
- Conftest evaluates the same `gate-input.json` with Rego in CI.
