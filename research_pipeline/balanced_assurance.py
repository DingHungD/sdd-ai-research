"""Executable contract harness for the balanced SDD assurance experiment."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


REQUIRED_INPUTS = {
    "openspec_requirements": "openspec/requirements.json",
    "openspec_change_proposal": "openspec/change-proposal.json",
    "openlore_context_graph": "openlore/context-graph.json",
    "openlore_drift_report": "openlore/drift-report.json",
    "cc_sdd_execution_plan": "cc-sdd/execution-plan.json",
    "cc_sdd_evidence_bundle": "cc-sdd/evidence-bundle.json",
    "security_controls": "policy/security-controls.yaml",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=True, indent=2)
        handle.write("\n")


def context_graph_digest(context_graph: dict[str, Any]) -> str:
    hashable_graph = copy.deepcopy(context_graph)
    hashable_graph.pop("graph_sha256", None)
    canonical = json.dumps(
        hashable_graph, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_gate_input(experiment_dir: Path) -> dict[str, Any]:
    loaded = {
        key: load_json(experiment_dir / relative_path)
        for key, relative_path in REQUIRED_INPUTS.items()
    }
    return {
        "schema_version": "1.0",
        "experiment": {
            "id": "balanced-assurance-poc",
            "stack": [
                "OpenSpec",
                "OpenLore",
                "cc-sdd",
                "OPA/Rego",
                "Conftest",
            ],
            "contract_mode": True,
        },
        "openspec": {
            "requirements": loaded["openspec_requirements"],
            "change_proposal": loaded["openspec_change_proposal"],
        },
        "openlore": {
            "context_graph": loaded["openlore_context_graph"],
            "drift_report": loaded["openlore_drift_report"],
        },
        "cc_sdd": {
            "execution_plan": loaded["cc_sdd_execution_plan"],
            "evidence_bundle": loaded["cc_sdd_evidence_bundle"],
        },
        "policy": {"security_controls": loaded["security_controls"]},
    }


def apply_overrides(
    gate_input: dict[str, Any], override_path: Path | None
) -> dict[str, Any]:
    if override_path is None:
        return gate_input
    overridden = copy.deepcopy(gate_input)
    for dotted_path, value in load_json(override_path).get("set", {}).items():
        segments = dotted_path.split(".")
        cursor: Any = overridden
        for segment in segments[:-1]:
            cursor = cursor[int(segment)] if isinstance(cursor, list) else cursor[segment]
        final_segment = segments[-1]
        if isinstance(cursor, list):
            cursor[int(final_segment)] = value
        else:
            cursor[final_segment] = value
    return overridden


def _finding(code: str, message: str, severity: str = "error") -> dict[str, str]:
    return {"code": code, "severity": severity, "message": message}


def evaluate_gate(gate_input: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    requirements = gate_input["openspec"]["requirements"]["requirements"]
    proposal = gate_input["openspec"]["change_proposal"]
    context_graph = gate_input["openlore"]["context_graph"]
    drift = gate_input["openlore"]["drift_report"]
    tasks = gate_input["cc_sdd"]["execution_plan"]["tasks"]
    evidence = gate_input["cc_sdd"]["evidence_bundle"]
    controls = gate_input["policy"]["security_controls"]["controls"]

    requirement_ids = [requirement["id"] for requirement in requirements]
    task_ids = {task["id"] for task in tasks}
    control_ids = {control["id"] for control in controls}
    test_results = {test["id"]: test for test in evidence["tests"]}
    review_results = {review["task_id"]: review for review in evidence["reviews"]}

    if len(requirement_ids) != len(set(requirement_ids)):
        findings.append(_finding("REQ_DUPLICATE", "Requirement IDs must be unique."))
    if proposal.get("approval", {}).get("status") != "approved":
        findings.append(
            _finding("PROPOSAL_UNAPPROVED", "OpenSpec change proposal needs approval.")
        )

    for requirement in requirements:
        requirement_id = requirement["id"]
        if requirement.get("status") != "approved":
            findings.append(
                _finding(
                    "REQ_UNAPPROVED",
                    f"{requirement_id} is not an approved requirement.",
                )
            )
        if not requirement.get("acceptance_criteria"):
            findings.append(
                _finding("REQ_NO_ACCEPTANCE", f"{requirement_id} has no acceptance criteria.")
            )
        for control_id in requirement.get("control_ids", []):
            if control_id not in control_ids:
                findings.append(
                    _finding(
                        "REQ_UNKNOWN_CONTROL",
                        f"{requirement_id} references unknown control {control_id}.",
                    )
                )
        if not any(requirement_id in task.get("requirement_ids", []) for task in tasks):
            findings.append(
                _finding(
                    "REQ_NO_TASK",
                    f"{requirement_id} has no cc-sdd implementation task.",
                )
            )
        for criterion in requirement.get("acceptance_criteria", []):
            for test_id in criterion.get("test_ids", []):
                if test_id not in test_results:
                    findings.append(
                        _finding(
                            "REQ_TEST_MISSING",
                            f"{criterion['id']} references missing test {test_id}.",
                        )
                    )
                elif test_results[test_id].get("status") != "passed":
                    findings.append(
                        _finding(
                            "REQ_TEST_FAILED",
                            f"{criterion['id']} is backed by non-passing test {test_id}.",
                        )
                    )

    for task in tasks:
        task_id = task["id"]
        if task.get("status") != "completed":
            findings.append(_finding("TASK_INCOMPLETE", f"{task_id} is not completed."))
        if not task.get("code_paths"):
            findings.append(_finding("TASK_NO_CODE", f"{task_id} has no code paths."))
        if not task.get("test_ids"):
            findings.append(_finding("TASK_NO_TEST", f"{task_id} has no test IDs."))
        if task_id not in review_results:
            findings.append(_finding("TASK_NO_REVIEW", f"{task_id} has no review evidence."))
        elif review_results[task_id].get("status") != "approved":
            findings.append(
                _finding("TASK_REVIEW_REJECTED", f"{task_id} review is not approved.")
            )

    for test in evidence["tests"]:
        if test.get("status") != "passed":
            findings.append(_finding("EVIDENCE_TEST_FAILED", f"{test['id']} did not pass."))

    actual_graph_sha256 = context_graph_digest(context_graph)
    if context_graph.get("graph_sha256") != actual_graph_sha256:
        findings.append(
            _finding(
                "CONTEXT_GRAPH_HASH_INVALID",
                "OpenLore context graph digest does not match its content.",
            )
        )
    if drift.get("current_graph_sha256") != context_graph.get("graph_sha256"):
        findings.append(
            _finding(
                "DRIFT_CONTEXT_MISMATCH",
                "OpenLore drift report does not describe the supplied context graph.",
            )
        )
    if drift.get("human_approval", {}).get("status") != "approved":
        findings.append(
            _finding("DRIFT_UNAPPROVED", "OpenLore drift report needs human approval.")
        )
    if drift.get("stale_nodes"):
        findings.append(
            _finding("DRIFT_STALE_NODE", "OpenLore reported stale repository nodes.")
        )
    if drift.get("orphan_nodes"):
        findings.append(
            _finding("DRIFT_ORPHAN_NODE", "OpenLore reported orphan repository nodes.")
        )
    if drift.get("baseline_graph_sha256") != drift.get("current_graph_sha256"):
        findings.append(
            _finding("DRIFT_HASH_CHANGED", "Repository graph differs from approved baseline.")
        )

    for control in controls:
        if not control.get("enforced"):
            findings.append(
                _finding("CONTROL_NOT_ENFORCED", f"{control['id']} is not enforced.")
            )

    errors = [finding for finding in findings if finding["severity"] == "error"]
    return {
        "schema_version": "1.0",
        "verdict": "pass" if not errors else "fail",
        "summary": {
            "requirement_count": len(requirements),
            "task_count": len(task_ids),
            "control_count": len(control_ids),
            "finding_count": len(findings),
            "error_count": len(errors),
        },
        "findings": findings,
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Balanced Assurance PoC Result",
        "",
        f"- Verdict: `{report['verdict']}`",
        f"- Requirements: `{summary['requirement_count']}`",
        f"- Tasks: `{summary['task_count']}`",
        f"- Controls: `{summary['control_count']}`",
        f"- Errors: `{summary['error_count']}`",
        "",
        "## Findings",
        "",
    ]
    if not report["findings"]:
        lines.append("- No blocking findings.")
    else:
        for finding in report["findings"]:
            lines.append(
                f"- `{finding['severity']}` `{finding['code']}`: {finding['message']}"
            )
    lines.append("")
    return "\n".join(lines)


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def run_conftest(input_path: Path, policy_dir: Path) -> tuple[str, str]:
    conftest = shutil.which("conftest")
    if conftest is None:
        return "unavailable", "conftest executable was not found on PATH"
    result = subprocess.run(
        [conftest, "test", str(input_path), "--policy", str(policy_dir)],
        check=False,
        capture_output=True,
        text=True,
    )
    output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
    return ("passed" if result.returncode == 0 else "failed"), output


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--experiment",
        type=Path,
        default=Path("experiments/balanced-assurance-poc"),
        help="Experiment directory containing OpenSpec, OpenLore, cc-sdd and policy artifacts.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Artifact output directory. Defaults to <experiment>/artifacts.",
    )
    parser.add_argument(
        "--overrides",
        type=Path,
        help="Optional JSON fixture with dotted paths to override before evaluation.",
    )
    parser.add_argument(
        "--require-conftest",
        action="store_true",
        help="Fail when the real Conftest executable is unavailable or rejects the input.",
    )
    parser.add_argument(
        "--skip-conftest",
        action="store_true",
        help="Run only the local Python verifier.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = create_parser().parse_args(argv)
    experiment_dir = args.experiment.resolve()
    output_dir = (args.output_dir or experiment_dir / "artifacts").resolve()
    gate_input = apply_overrides(build_gate_input(experiment_dir), args.overrides)
    report = evaluate_gate(gate_input)
    gate_input_path = output_dir / "gate-input.json"
    report_path = output_dir / "assurance-report.json"
    write_json(gate_input_path, gate_input)
    write_json(report_path, report)
    write_markdown(output_dir / "assurance-report.md", render_markdown(report))

    conftest_status = "skipped"
    conftest_output = ""
    if not args.skip_conftest:
        conftest_status, conftest_output = run_conftest(
            gate_input_path, experiment_dir / "policy"
        )

    print(f"Local verifier: {report['verdict']}")
    print(f"Conftest: {conftest_status}")
    if conftest_output:
        print(conftest_output)
    print(f"Report: {report_path}")

    if report["verdict"] != "pass":
        return 1
    if args.require_conftest and conftest_status != "passed":
        return 1
    if conftest_status == "failed":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
