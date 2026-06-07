from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path


import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research_pipeline.agent_tasks import (  # noqa: E402
    block_task,
    complete_task,
    create_task,
    fail_task,
    load_task,
    start_task,
    validate_task,
    validate_task_result,
)
from research_pipeline.io_utils import read_json, write_json  # noqa: E402
from research_pipeline.repo_manifest import build_repo_manifest  # noqa: E402


class ResearchPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="research-pipeline-test-"))
        self.topic_id = "fixture-topic"
        self.topic_dir = self.temp_dir / "knowledge-base" / "topics" / self.topic_id
        self.topic_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_valid_subagent_task_passes(self) -> None:
        task = create_task(
            self.topic_dir,
            topic_id=self.topic_id,
            agent_role="source_curator_agent",
            objective="Curate fixture source.",
            paths_or_urls=["knowledge-base/topics/fixture-topic/sources/S-001/source.json"],
            source_ids=["S-001"],
        )

        self.assertEqual([], validate_task(task))
        self.assertTrue((self.topic_dir / "agent-tasks" / "T-001.json").exists())

    def test_missing_expected_output_fails(self) -> None:
        task = create_task(
            self.topic_dir,
            topic_id=self.topic_id,
            agent_role="source_curator_agent",
            objective="Curate fixture source.",
        )
        del task["expected_output"]

        self.assertIn("missing required field: expected_output", validate_task(task))

    def test_invalid_agent_role_fails(self) -> None:
        task = {
            "task_id": "T-001",
            "topic_id": self.topic_id,
            "agent_role": "unknown_agent",
            "model": "gpt-5.4",
            "reasoning_effort": "medium",
            "objective": "Invalid role.",
            "input": {"paths_or_urls": [], "questions": ["Invalid role."], "constraints": []},
            "expected_output": {"artifact_type": "document_summary", "schema": "x", "required_fields": ["summary"]},
            "write_scope": {"allowed_paths": [], "forbidden_paths": []},
            "quality_gate": {"checks": ["check"], "done_when": ["done"]},
            "status": "pending",
        }

        self.assertIn("invalid agent_role: unknown_agent", validate_task(task))

    def test_github_repo_task_requires_repo_related_input(self) -> None:
        task = create_task(
            self.topic_dir,
            topic_id=self.topic_id,
            agent_role="github_repo_analyst_agent",
            objective="Analyze GitHub repo.",
        )
        task["input"]["source_ids"] = []
        task["input"]["paths_or_urls"] = []

        self.assertIn(
            "github_repo_analyst_agent task requires source_ids or paths_or_urls",
            validate_task(task),
        )

    def test_task_complete_validates_result_required_fields(self) -> None:
        task = create_task(
            self.topic_dir,
            topic_id=self.topic_id,
            agent_role="source_curator_agent",
            objective="Curate fixture source.",
            source_ids=["S-001"],
        )
        errors = validate_task_result(task, {"status": "completed", "summary": "Only summary."})

        self.assertIn("result missing required field for completed task: document_purpose", errors)
        self.assertIn("result missing required field for completed task: key_points", errors)

    def test_task_complete_records_valid_result(self) -> None:
        task = create_task(
            self.topic_dir,
            topic_id=self.topic_id,
            agent_role="source_curator_agent",
            objective="Curate fixture source.",
            source_ids=["S-001"],
        )
        result = {
            "status": "completed",
            "document_purpose": "Purpose.",
            "summary": "Summary.",
            "key_points": [{"point": "Point.", "locator": "fixture"}],
            "keywords": ["fixture"],
            "limitations": ["Synthetic fixture."],
        }

        completed = complete_task(self.topic_dir, task["task_id"], result)

        self.assertEqual("completed", completed["status"])
        self.assertEqual(result, load_task(self.topic_dir, task["task_id"])["result"])

    def test_task_start_block_and_fail_update_status(self) -> None:
        task = create_task(
            self.topic_dir,
            topic_id=self.topic_id,
            agent_role="source_curator_agent",
            objective="Curate fixture source.",
            source_ids=["S-001"],
        )

        started = start_task(self.topic_dir, task["task_id"])
        self.assertEqual("in_progress", started["status"])

        blocked = block_task(self.topic_dir, task["task_id"], "Need human scope decision.")
        self.assertEqual("blocked", blocked["status"])
        self.assertEqual("Need human scope decision.", blocked["human_escalation_reason"])

        failed = fail_task(self.topic_dir, task["task_id"], "Fixture failure.")
        self.assertEqual("failed", failed["status"])
        self.assertEqual(["Fixture failure."], failed["result"]["errors"])

    def test_repo_manifest_updates_github_source_metadata(self) -> None:
        fixture = ROOT / "tests" / "fixtures" / "github-repo-source" / "source.json"
        source_dir = self.topic_dir / "sources" / "S-001"
        source_dir.mkdir(parents=True)
        write_json(source_dir / "source.json", read_json(fixture))

        manifest = build_repo_manifest(self.topic_dir, "S-001")
        source = read_json(source_dir / "source.json")

        self.assertEqual("selected_files", manifest["capture_strategy"])
        self.assertEqual("a2aproject", manifest["repository"]["owner"])
        self.assertEqual("A2A", manifest["repository"]["name"])
        self.assertTrue((source_dir / "repo-manifest.json").exists())
        self.assertEqual("selected_files", source["repository"]["capture_scope"])
        self.assertEqual("sources/S-001/repo-manifest.json", source["repository"]["capture_manifest_path"])
        self.assertFalse(manifest["needs_commit_pin"])
        self.assertIn("candidate_files", manifest)
        self.assertIn("selected_files", manifest)

    def test_repo_manifest_marks_needs_commit_pin(self) -> None:
        fixture = ROOT / "tests" / "fixtures" / "github-repo-source-no-commit" / "source.json"
        source_dir = self.topic_dir / "sources" / "S-001"
        source_dir.mkdir(parents=True)
        write_json(source_dir / "source.json", read_json(fixture))

        manifest = build_repo_manifest(self.topic_dir, "S-001")
        source = read_json(source_dir / "source.json")

        self.assertTrue(manifest["needs_commit_pin"])
        self.assertIn("commit SHA", manifest["blocked_reason"])
        self.assertTrue(source["repository"]["needs_commit_pin"])

    def test_repo_manifest_creates_blocked_task_for_monorepo_scope(self) -> None:
        fixture = ROOT / "tests" / "fixtures" / "github-monorepo-source" / "source.json"
        source_dir = self.topic_dir / "sources" / "S-001"
        source_dir.mkdir(parents=True)
        write_json(source_dir / "source.json", read_json(fixture))

        manifest = build_repo_manifest(self.topic_dir, "S-001")
        tasks = list((self.topic_dir / "agent-tasks").glob("T-*.json"))
        task = read_json(tasks[0])

        self.assertIn("monorepo", manifest["blocked_reason"])
        self.assertEqual("blocked", task["status"])
        self.assertEqual("github_repo_analyst_agent", task["agent_role"])
        self.assertEqual(["S-001"], task["input"]["source_ids"])

    def test_readme_only_github_fixture_is_positioning_only(self) -> None:
        summary = json.loads((ROOT / "tests" / "fixtures" / "readme-only-github-summary.json").read_text(encoding="utf-8"))

        self.assertIn("positioning", summary["summary"])
        self.assertTrue(any("No source" in item for item in summary["limitations"]))


if __name__ == "__main__":
    unittest.main()
