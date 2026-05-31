# Balanced Assurance PoC Results

## Scope

This is the first executable experiment for the balanced robust stack:

`OpenSpec + OpenLore + cc-sdd + OPA/Rego + Conftest`

The experiment assumes that an SDD already exists. It validates the handoff
contracts and merge gate, rather than installing long-running upstream agents.

## Executed Cases

| Case | Python verifier | Conftest/Rego | Expected result |
| --- | --- | --- | --- |
| Approved baseline | Pass | `10 tests, 10 passed` | Merge allowed |
| Stale node and failed test | Fail | `8 passed, 2 failures` | Merge blocked |

The blocked Rego case reports:

- `AC-002 is not backed by passing test TC-002`
- `OpenLore reported stale repository nodes`

## What Is Implemented

- Existing SDD document mapped to versioned OpenSpec-style requirement IDs.
- Approved change proposal with a human approval artifact.
- OpenLore-style repository graph, canonical digest validation, drift report,
  impact analysis and human drift approval.
- cc-sdd-style boundary-aware tasks, test evidence and independent review
  evidence.
- JSON-compatible `security-controls.yaml`, Rego policy and Conftest CI gate.
- Dependency-free Python verifier for immediate local execution.
- Passing and intentionally failing generated assurance reports.

## Limits

- OpenSpec, OpenLore and cc-sdd are represented by replaceable contracts; their
  upstream CLIs or daemons are not invoked by this repository yet.
- The graph is a small fixture. A brownfield trial should replace it with
  repository analysis output from a real service.
- The control pack validates traceability, drift and evidence. A production
  policy pack still needs organization-specific security rules.

## Next Experiment

Run the same gate against one real brownfield repository. Import actual
OpenLore graph output, map one approved OpenSpec change into cc-sdd tasks, and
record setup cost, drift precision, false blocks and maintenance effort.
