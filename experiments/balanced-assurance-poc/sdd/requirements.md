# Example SDD: Reliable Merge Gate

This document stands in for an existing SDD. The experiment does not generate
the requirements; it tests whether downstream artifacts remain traceable.

## REQ-001 Traceability

Every approved requirement must map to an implementation task, code path,
test result and independent review evidence.

## REQ-002 Brownfield Drift

A merge must be blocked when the repository graph contains stale or orphan
nodes, or when the graph differs from the approved baseline.

## REQ-003 Policy Gate

The PR and deploy path must execute versioned security controls through a
structured policy input.
