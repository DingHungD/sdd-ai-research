package main

import rego.v1

deny contains msg if {
	some requirement in input.openspec.requirements.requirements
	requirement.status != "approved"
	msg := sprintf("%s is not approved", [requirement.id])
}

deny contains msg if {
	input.openspec.change_proposal.approval.status != "approved"
	msg := "OpenSpec change proposal needs approval"
}

deny contains msg if {
	some requirement in input.openspec.requirements.requirements
	not requirement_has_task(requirement.id)
	msg := sprintf("%s has no cc-sdd implementation task", [requirement.id])
}

deny contains msg if {
	some criterion in input.openspec.requirements.requirements[_].acceptance_criteria
	some test_id in criterion.test_ids
	not passed_test(test_id)
	msg := sprintf("%s is not backed by passing test %s", [criterion.id, test_id])
}

deny contains msg if {
	count(input.openlore.drift_report.stale_nodes) > 0
	msg := "OpenLore reported stale repository nodes"
}

deny contains msg if {
	count(input.openlore.drift_report.orphan_nodes) > 0
	msg := "OpenLore reported orphan repository nodes"
}

deny contains msg if {
	input.openlore.drift_report.baseline_graph_sha256 != input.openlore.drift_report.current_graph_sha256
	msg := "Repository graph differs from approved baseline"
}

deny contains msg if {
	input.openlore.drift_report.current_graph_sha256 != input.openlore.context_graph.graph_sha256
	msg := "OpenLore drift report does not describe the supplied context graph"
}

deny contains msg if {
	input.openlore.drift_report.human_approval.status != "approved"
	msg := "OpenLore drift report needs human approval"
}

deny contains msg if {
	some control in input.policy.security_controls.controls
	not control.enforced
	msg := sprintf("%s is not enforced", [control.id])
}

requirement_has_task(requirement_id) if {
	some task in input.cc_sdd.execution_plan.tasks
	requirement_id in task.requirement_ids
}

passed_test(test_id) if {
	some test in input.cc_sdd.evidence_bundle.tests
	test.id == test_id
	test.status == "passed"
}
