from pathlib import Path
import tempfile
import unittest

from research_pipeline.balanced_assurance import (
    apply_overrides,
    build_gate_input,
    evaluate_gate,
    main,
)


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments" / "balanced-assurance-poc"


class BalancedAssuranceTest(unittest.TestCase):
    def test_passing_contract(self) -> None:
        report = evaluate_gate(build_gate_input(EXPERIMENT))

        self.assertEqual("pass", report["verdict"])
        self.assertEqual([], report["findings"])

    def test_drift_and_failed_test_block_merge(self) -> None:
        gate_input = apply_overrides(
            build_gate_input(EXPERIMENT),
            EXPERIMENT / "fixtures" / "failing-overrides.json",
        )

        report = evaluate_gate(gate_input)
        codes = {finding["code"] for finding in report["findings"]}

        self.assertEqual("fail", report["verdict"])
        self.assertIn("DRIFT_STALE_NODE", codes)
        self.assertIn("REQ_TEST_FAILED", codes)
        self.assertIn("EVIDENCE_TEST_FAILED", codes)

    def test_cli_writes_artifacts_without_conftest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_dir = Path(temporary_directory)
            exit_code = main(
                [
                    "--experiment",
                    str(EXPERIMENT),
                    "--output-dir",
                    str(output_dir),
                    "--skip-conftest",
                ]
            )

            self.assertEqual(0, exit_code)
            self.assertTrue((output_dir / "gate-input.json").exists())
            self.assertTrue((output_dir / "assurance-report.json").exists())
            self.assertTrue((output_dir / "assurance-report.md").exists())


if __name__ == "__main__":
    unittest.main()
