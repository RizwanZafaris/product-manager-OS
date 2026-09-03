#!/usr/bin/env python3
"""Immutable verifier registry for the readiness evaluator.

The JSON rubric names opaque verifier ids.  It cannot inject a shell command,
weaken an expected test count, or turn a check into ``true``.  Reviewers can
therefore audit this small code registry separately from point allocation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    """One argv-only check and, for unittest, the exact tests it must run."""

    argv: tuple
    tests: tuple = ()
    timeout: int = 900


def unit(*test_ids):
    return Step(("python3", "-m", "unittest", *test_ids, "-v"),
                tuple(test_ids))


def probe(name, timeout=900):
    return Step(("python3", "tools/readiness_probe.py", name),
                timeout=timeout)


DOMAIN_TESTS = tuple(
    "test_pmos_domain.DomainTest." + name for name in (
        "test_lifecycle_e2e_and_independent_stages",
        "test_blocked_transition_and_cas",
        "test_transition_requires_current_stage_gate_not_old_assertions",
        "test_traceability_is_typed_and_non_dangling",
        "test_rbac_and_collaboration",
        "test_reserved_system_actor_and_unguarded_writes_are_rejected",
        "test_new_product_atomically_grants_creator_ownership",
        "test_cross_product_reads_and_dependencies_respect_authority_boundary",
        "test_generic_create_and_update_cannot_bypass_governance",
        "test_approval_requires_independent_approver_and_persists_requester",
        "test_regulated_approval_drift_revoke_and_reapprove",
        "test_gate_rejects_labels_cross_initiative_evidence_and_hash_drift",
        "test_digest_only_evidence_requires_external_verification",
        "test_gate_completion_is_revisioned_and_concurrent_proof_conflicts",
        "test_regulated_checkpoint_requires_current_independent_bound_approval",
        "test_audit_export_redacts_evidence_and_collaboration_content",
        "test_capacity_priority_sequence_dependencies_and_audit",
        "test_full_aggregate_round_trip_rehydrates_every_state_family",
        "test_two_instances_conflict_rolls_back_then_refresh_retry_preserves_both",
        "test_tampered_hash_and_unknown_schema_fail_closed",
        "test_every_public_mutator_is_transactional",
    ))

CONDUCTOR_TESTS = tuple(
    "test_pmos_conductor.ConductorTest." + name for name in (
        "test_three_turns_survive_reopen_and_subprocess_exit",
        "test_invalid_does_not_advance_and_challenge_is_capped",
        "test_duplicate_turn_and_stale_revision_are_explicit",
        "test_completion_requires_answers_and_each_gate",
        "test_gate_proof_requires_authority_independence_and_verified_hash",
        "test_question_bank_freezes_all_sequences",
        "test_evicted_turn_is_state_checked_and_window_does_not_permanently_block",
    ))

ROUTING_TESTS = tuple(
    "test_pmos_routing.RoutingTests." + name for name in (
        "test_success_and_allowlisted_provenance",
        "test_provider_reported_substitution_fails_before_confidential_data_is_accepted",
        "test_provider_missing_actual_model_identity_fails_closed",
        "test_refusal_rate_limit_timeout_and_network_use_bounded_fallback",
        "test_unavailable_provider_and_model_are_skipped",
        "test_privacy_capability_tool_context_latency_and_budget_are_policy_filters",
        "test_budget_reserves_fallbacks_and_rejects_provider_overspend",
        "test_budget_counts_policy_failed_paid_attempts_before_fallback",
        "test_authoritative_usage_cannot_overrun_context_or_lie_about_total",
        "test_discovery_failure_is_bounded_and_never_leaks_exception_text",
        "test_actual_and_wall_latency_are_enforced_and_timeout_is_forwarded",
        "test_missing_usage_cannot_hide_an_oversized_output",
        "test_model_metadata_rejects_truthy_strings_and_string_collections",
        "test_privacy_permission_cannot_downgrade_data_classification",
        "test_free_or_uncertified_models_are_rejected_for_high_risk",
        "test_dynamic_catalog_and_fallback_exhaustion_are_deterministic",
        "test_no_eligible_model_is_explicitly_blocked",
        "test_secret_store_repr_and_provider_failures_never_leak",
    ))

HOOK_TESTS = tuple(
    "test_pmos_hooks.ClaudeHookTests." + name for name in (
        "test_project_settings_wire_every_required_loop_event",
        "test_safe_write_is_allowed_and_escape_or_protected_write_is_denied",
        "test_destructive_command_is_denied_and_external_write_asks",
        "test_unknown_mcp_tools_never_default_to_allow",
        "test_unknown_or_case_mismatched_tools_never_default_to_allow",
        "test_external_command_variants_require_approval",
        "test_shell_classification_fails_closed_on_ambiguous_or_destructive_text",
        "test_unknown_interpreters_network_and_redirection_default_to_approval",
        "test_untrusted_instruction_cannot_authorize_tool_use",
        "test_secret_is_blocked_and_never_copied_to_audit_or_output",
        "test_claude_event_specific_output_contracts",
        "test_command_adapter_fails_closed_on_malformed_json",
    )) + tuple(
        "test_pmos_hooks.RuntimeHookTests." + name for name in (
            "test_transition_requires_actor_revision_and_evidence",
            "test_commit_provider_and_external_boundaries_fail_closed",
            "test_runtime_boundaries_reject_malformed_or_truthy_bypasses",
            "test_completion_hook_blocks_a_failed_release_gate",
            "test_hook_bus_is_ordered_and_stops_after_denial",
        ))

STORE_TESTS = tuple(
    "test_pmos_store.StoreTest." + name for name in (
        "test_pragmas_and_atomic_full_snapshot_commit",
        "test_stale_compare_and_swap_is_an_explicit_conflict",
        "test_concurrent_local_writers_and_reader_snapshot",
        "test_one_store_instance_serializes_concurrent_callers",
        "test_reopen_prepared_and_published_crash_boundaries",
        "test_process_kill_commit_boundaries_are_atomic",
        "test_cross_store_commit_pack_and_stale_conflict",
        "test_pack_rejects_corruption_and_traversal",
        "test_queue_dedup_fencing_heartbeat_retry_cancel_and_deadletter",
        "test_queue_recovers_expired_leases_and_commits_one_result",
        "test_queue_projection_and_event_tampering_fail_before_dispatch",
        "test_queue_integrity_migration_backfills_once_but_never_reblesses_deletion",
        "test_task_memory_isolation_classes_promotion_rebuild_and_tamper",
        "test_memory_projection_drift_fails_verification_and_rebuild_repairs",
        "test_backup_restore_and_verify",
        "test_expired_leases_cannot_heartbeat_or_finish_without_recovery_call",
        "test_database_backup_and_restore_reject_symlink_or_special_targets",
        "test_backup_and_restore_connect_boundaries_reject_parent_swaps",
        "test_connect_boundary_parent_swap_never_creates_or_uses_external_database",
        "test_nonfinal_ancestor_swap_cannot_redirect_guard_open",
        "test_relative_and_uri_metacharacter_database_names_are_literal",
        "test_post_initialization_database_parent_swap_fails_before_operation",
        "test_forged_missing_or_cross_product_head_fails_closed",
    ))

OPERATIONS_TESTS = (
    "test_pmos_operations.AdapterContractTests.test_all_five_in_memory_adapters_share_versioned_contract",
    "test_pmos_operations.AdapterContractTests.test_bad_adapter_fails_closed",
    "test_pmos_operations.OutboxTests.test_idempotency_conflict_retry_dead_letter_and_reconcile",
    "test_pmos_operations.OutboxTests.test_degraded_and_unavailable_modes_are_explicit",
    "test_pmos_operations.OutboxTests.test_delivered_event_is_not_resent_and_sender_gets_idempotency_envelope",
    "test_pmos_operations.OutboxTests.test_acknowledgement_requires_a_delivered_matching_record",
    "test_pmos_operations.OutboxTests.test_sender_identity_secret_content_and_concurrent_attempts_fail_closed",
    "test_pmos_operations.AnalyticsTests.test_metric_freshness_future_and_lineage",
    "test_pmos_operations.AnalyticsTests.test_experiment_outcome_links_typed_experiment_and_decision",
    "test_pmos_operations.ResearchTests.test_consent_recruit_retention_redaction_deletion_and_quote_refusal",
    "test_pmos_operations.ResearchTests.test_quote_needs_explicit_quote_scope_and_retention",
    "test_pmos_operations.ResearchTests.test_future_research_capture_and_pre_capture_reads_fail_closed",
    "test_pmos_operations.ResearchTests.test_expired_consent_blocks_storage_reads_before_retention_expiry",
    "test_pmos_operations.ResearchTests.test_public_evidence_view_hides_expired_and_withdrawn_content",
    "test_pmos_operations.ResearchTests.test_consent_scope_timestamps_and_secret_evidence_fail_closed",
    "test_pmos_operations.AdoptionTests.test_observation_requires_consent_and_does_not_claim_external_adoption",
    "test_pmos_operations.AdoptionTests.test_consent_and_accessibility_flags_require_exact_booleans",
    "test_pmos_operations.OperationsBoundaryTests.test_issue_updates_allow_only_valid_mutable_fields",
    "test_pmos_operations.OperationsBoundaryTests.test_bounded_in_memory_adapters_reject_oversized_record_sets",
)

USE_CASE_TESTS = tuple(
    "test_pmos_usecases.UseCaseMatrixTests." + name for name in (
        "test_registry_is_exactly_the_mandatory_thirteen",
        "test_every_registered_case_executes_and_returns_behavioral_evidence",
        "test_unknown_case_is_rejected",
        "test_self_attested_or_always_passing_stub_cannot_satisfy_matrix",
    ))

REVIEW_TESTS = tuple(
    "test_pmos_review.IndependentReviewGateTests." + name for name in (
        "test_exact_tree_review_passes_and_any_content_change_stales_it",
        "test_nested_build_or_dist_named_source_is_part_of_exact_tree",
        "test_parent_swap_uses_pinned_review_tree_descriptor",
        "test_nested_directory_replacement_during_inventory_fails_closed",
        "test_symlink_replacement_during_inventory_fails_closed",
        "test_whole_root_swap_fails_closed",
        "test_unresolved_high_priority_finding_fails",
        "test_review_cannot_be_self_declared_or_use_unknown_fields",
        "test_local_record_cannot_claim_authenticated_reviewer_identity",
    ))

OPENROUTER_TESTS = tuple(
    "test_pmos_skills.OpenRouterTests." + name for name in (
        "test_catalog_parses_models_and_free_pricing",
        "test_chat_uses_exact_id_and_actual_model",
        "test_auth_absence_429_malformed_and_oversize_are_safe",
        "test_base_url_override_requires_an_exact_trusted_https_host",
        "test_insecure_test_transport_is_loopback_injected_and_credential_free",
        "test_cross_origin_or_redirect_response_is_rejected",
        "test_dynamic_discovery_failure_is_safe_and_honors_request_timeout",
        "test_completion_requires_usage_and_enforces_output_and_timeout_caps",
        "test_router_supplied_environment_secret_is_used_without_retention",
    ))

SKILL_TESTS = tuple(
    "test_pmos_skills.SkillRegistryTests." + name for name in (
        "test_shipped_runtime_contracts_are_complete_and_deterministic",
        "test_unknown_field_and_hash_drift_fail_closed",
        "test_trusted_manifest_blocks_self_approved_graph_contract_and_risk_edits",
        "test_unknown_extra_skill_asset_and_symlink_fail_closed",
        "test_trusted_manifest_symlink_and_path_escape_fail_closed",
    ))

SECURITY_TESTS = (
    "test_pmos_security.SecurityGateFixtureTests.test_clean_fixture_passes_and_each_static_violation_fails",
    "test_pmos_security.SecurityGateFixtureTests.test_threat_model_and_dependency_exceptions_are_required",
    "test_pmos_security.SecurityGateFixtureTests.test_aliases_import_from_dynamic_dispatch_and_nonliteral_shell_fail_closed",
    "test_pmos_security.DocumentationContractFixtureTests.test_clean_fixture_passes_and_readme_warning_is_actionable",
    "test_pmos_security.DocumentationContractFixtureTests.test_mutations_prove_heading_alt_link_boundary_and_claim_failures",
    "test_pmos_security.PublicRuntimeAdversarialTests.test_untrusted_prompt_cannot_authorize_tool_and_secret_never_leaks",
    "test_pmos_security.PublicRuntimeAdversarialTests.test_store_rejects_traversal_before_persistence",
    "test_pmos_security.PublicRuntimeAdversarialTests.test_audit_tamper_and_regulated_approval_drift_fail_closed",
)

EVALUATOR_TESTS = (
    "test_readiness.RubricValidationTests.test_category_criteria_sum_mismatch_fails",
    "test_readiness.RubricValidationTests.test_criterion_naming_unknown_task_fails",
    "test_readiness.RubricValidationTests.test_duplicate_criterion_ids_fail",
    "test_readiness.RubricValidationTests.test_external_policy_cannot_self_attest",
    "test_readiness.RubricValidationTests.test_legacy_task_ledger_schema_is_rejected",
    "test_readiness.RubricValidationTests.test_legacy_verify_shell_string_is_rejected_without_execution",
    "test_readiness.RubricValidationTests.test_marker_file_injection_in_json_is_never_executed",
    "test_readiness.RubricValidationTests.test_missing_task_ownership_fails",
    "test_readiness.RubricValidationTests.test_non_100_total_fails",
    "test_readiness.RubricValidationTests.test_task_dependency_cycle_is_rejected",
    "test_readiness.RubricValidationTests.test_task_owning_nothing_fails",
    "test_readiness.RubricValidationTests.test_unknown_criterion_owned_by_task_fails",
    "test_readiness.RubricValidationTests.test_unknown_fields_fail_at_each_rubric_level",
    "test_readiness.RubricValidationTests.test_unknown_verifier_id_is_rejected_without_execution",
    "test_readiness.VerdictAndOutputTests.test_category_verdict_is_diagnostic_and_never_complete",
    "test_readiness.VerdictAndOutputTests.test_local_100_still_reports_external_readiness_as_blocked",
    "test_readiness.VerdictAndOutputTests.test_non_point_bearing_hard_gate_is_executed_and_can_be_green",
    "test_readiness.VerdictAndOutputTests.test_git_failure_never_looks_like_a_clean_exact_tree",
    "test_readiness.VerdictAndOutputTests.test_output_path_permits_external_temp_path",
    "test_readiness.VerdictAndOutputTests.test_output_path_rejects_unignored_repository_path",
    "test_readiness.VerifierExecutionTests.test_expected_failure_evidence_fails",
    "test_readiness.VerifierExecutionTests.test_missing_test_id_evidence_fails",
    "test_readiness.VerifierExecutionTests.test_run_verifier_uses_argv_and_shell_false",
    "test_readiness.VerifierExecutionTests.test_skip_evidence_fails",
    "test_readiness.VerifierExecutionTests.test_wrong_test_count_evidence_fails",
    "test_readiness.VerifierExecutionTests.test_zero_test_evidence_fails",
)

CLI_TESTS = tuple(
    "test_pmos_cli.CliTests." + name for name in (
        "test_init_status_verify_human_and_json",
        "test_user_supplied_evidence_flow_rejects_invalid_and_stale_submissions",
        "test_actionable_missing_runtime_error_is_json",
        "test_runtime_directory_symlink_never_escapes_workspace",
        "test_runtime_database_symlink_never_escapes_workspace",
        "test_gate_source_verifier_rejects_escape_symlink_and_hash_drift",
        "test_migration_dry_run_backup_atomic_activation_and_rollback",
        "test_destination_migration_lock_rejects_overlapping_activation_and_preserves_manifest_hash",
        "test_destination_migration_lock_rejects_symlink_lock_file",
        "test_destination_migration_lock_rejects_runtime_directory_swap",
        "test_destination_migration_lock_rejects_whole_destination_swap",
        "test_recovery_rejects_symlinked_migration_journal",
        "test_recovery_rejects_migration_journal_swapped_during_read",
        "test_rollback_rejects_runtime_directory_swap_and_symlinked_manifest",
        "test_recover_finalizes_sigkill_after_replace_existing_and_fresh",
        "test_recover_finalizes_sigkill_after_rollback_activation",
        "test_planned_file_symlink_swap_and_migration_limits_fail_closed",
        "test_recovery_and_rollback_refuse_unknown_active_runtime",
        "test_isolated_install_imports_console_script",
    ))

RELEASE_TESTS = tuple(
    "test_pmos_release.ReleaseProvenanceTests." + name for name in (
        "test_package_metadata_versions_are_identical",
        "test_safe_symlink_round_trip_and_worktree_git_file_are_supported",
        "test_regular_file_symlink_swap_during_hashing_fails_closed",
        "test_nested_directory_replacement_during_inventory_fails_closed",
        "test_symlink_replacement_during_inventory_fails_closed",
        "test_hashes_categories_and_detects_tampering",
        "test_mapping_manifest_cannot_exclude_a_self_chosen_file",
        "test_nested_runtime_named_directories_are_not_excluded",
        "test_output_is_json_without_content_or_secret",
        "test_output_parent_swap_cannot_redirect_provenance_write",
        "test_source_commit_is_bound_to_clean_current_git_head",
        "test_dirty_tree_is_never_attributed_to_head",
        "test_secret_like_path_blocks_build_and_cannot_hide_from_verification",
    ))


REGISTRY = {
    "os-tree": (Step(("python3", "lint.py", "--os")),),
    "workspace-lifecycle": (probe("workspace-lifecycle"),),
    "workspace-contract": (
        Step(("python3", "tools/check_workspace_contract.py", "--quiet")),),
    "workspace-links": (probe("workspace-links"),),
    "workspace-drift": (
        probe("workspace-drift"),
        unit(
            "harness.test_runner.AuditRegressionTests."
            "test_a_link_prefers_the_workspace_copy_over_the_blank_template",
        ),
    ),
    "link-grammar": (probe("link-grammar"),),
    "manifest-contract": (
        Step(("python3", "tools/check_manifest.py", "--quiet")),),
    "harness-route-behavior": (unit(
        "harness.test_runner.AuditRegressionTests."
        "test_every_route_declares_a_kind_the_runner_implements",
        "harness.test_runner.AuditRegressionTests."
        "test_a_route_with_no_declared_kind_is_refused",
        "harness.test_runner.AuditRegressionTests."
        "test_the_conductor_is_interactive_and_files_no_document",
        "harness.test_runner.AuditRegressionTests."
        "test_an_interactive_route_is_never_told_to_return_a_document",
    ),),
    "claude-adapter": (
        Step(("python3", "harness/adapters/claude-code/generate.py",
              "--check")),),
    "desktop-adapter": (
        Step(("python3", "harness/adapters/desktop/selftest.py")),),
    "commit-rollback": (unit(
        "harness.test_runner.AuditRegressionTests."
        "test_a_failed_commit_leaves_the_workspace_as_it_was",
        "harness.test_runner.AuditRegressionTests."
        "test_a_failed_commit_removes_a_file_that_did_not_exist_before",
    ),),
    "journal-concurrency": (unit(
        "harness.test_runner.AuditRegressionTests."
        "test_concurrent_journal_writers_keep_every_row",
        "harness.test_runner.AuditRegressionTests."
        "test_the_state_lock_refuses_rather_than_overwriting",
    ),),
    "deferred-job-record": (unit(
        "harness.test_runner.QueueOutcomeTests."
        "test_a_queued_run_leaves_a_job_record_that_can_be_listed",
        "harness.test_runner.QueueOutcomeTests."
        "test_a_certification_mismatch_queues_and_writes_no_artifact",
        "harness.test_runner.QueueOutcomeTests."
        "test_the_cap_queues_before_any_model_call",
        "harness.test_runner.QueueOutcomeTests."
        "test_a_tier_with_no_target_queues_rather_than_failing",
        "harness.test_runner.QueueOutcomeTests."
        "test_judgment_on_the_cli_transport_queues",
    ),),
    "domain-runtime": (unit(*DOMAIN_TESTS),),
    "conductor-runtime": (unit(*CONDUCTOR_TESTS),),
    "model-routing": (unit(*ROUTING_TESTS),),
    "openrouter-provider": (unit(*OPENROUTER_TESTS),),
    "claude-hooks": (unit(*HOOK_TESTS),),
    "runtime-hooks": (unit(*HOOK_TESTS),),
    "runtime-skills": (unit(*SKILL_TESTS),),
    "store-runtime": (unit(*STORE_TESTS),),
    "store-crash-recovery": (unit(
        "test_pmos_store.StoreTest."
        "test_process_kill_commit_boundaries_are_atomic",
    ),),
    "operations-runtime": (unit(*OPERATIONS_TESTS),),
    "usecase-matrix": (unit(*USE_CASE_TESTS),),
    "security-policy": (
        unit(*SECURITY_TESTS),
        Step(("python3", "tools/security_gate.py")),
    ),
    "docs-contract": (
        Step(("python3", "tools/docs_contract.py", "--strict")),),
    "accessibility": (
        unit(
            "test_pmos_security.DocumentationContractFixtureTests."
            "test_clean_fixture_passes_and_readme_warning_is_actionable",
            "test_pmos_security.DocumentationContractFixtureTests."
            "test_mutations_prove_heading_alt_link_boundary_and_claim_failures",
        ),
        Step(("python3", "tools/docs_contract.py", "--strict")),
    ),
    "evaluator-integrity": (unit(*EVALUATOR_TESTS),),
    "cli-contract": (unit(*CLI_TESTS),),
    "packaging-release": (unit(*(CLI_TESTS + RELEASE_TESTS)),),
    "approved-evidence": (unit(
        "test_lint.ReviewGateTests."
        "test_approved_with_an_unticked_box_fails",
    ),),
    "required-gate-section": (unit(
        "test_lint.ReviewGateTests."
        "test_missing_required_section_is_flagged",
    ),),
    "metric-provenance": (unit(
        "test_lint.WorkspaceModeTests."
        "test_a_sourced_example_number_passes_in_a_workspace",
        "test_lint.WorkspaceModeTests."
        "test_an_unsourced_example_number_still_fails_in_a_workspace",
    ),),
    "secret-boundaries": (unit(
        "test_lint.SecretGateTests.test_modern_token_formats_are_caught",
        "test_lint.SecretGateTests."
        "test_an_aws_secret_access_key_value_is_caught",
        "test_lint.SecretGateTests."
        "test_a_high_entropy_value_under_a_credential_name_is_caught",
        "test_lint.SecretGateTests."
        "test_a_base64_wrapped_token_is_caught",
        "test_lint.SecretGateTests."
        "test_a_token_split_across_a_line_break_is_caught",
        "test_lint.SecretGateTests."
        "test_a_rule_bearing_file_is_not_exempt_from_the_secret_gate",
        "test_lint.WorkspaceModeTests.test_a_secret_is_caught",
        "test_lint.WorkspaceModeTests."
        "test_a_secret_in_a_non_markdown_file_is_caught",
        "harness.test_runner.RedactionTests."
        "test_a_custom_variable_name_is_redacted",
        "harness.test_runner.RedactionTests.test_a_short_value_is_redacted",
        "harness.test_runner.RedactionTests."
        "test_a_short_credential_is_announced_on_stderr",
        "harness.test_runner.RedactionTests."
        "test_the_longest_value_is_masked_first",
        "harness.test_runner.RedactionTests."
        "test_safe_url_drops_userinfo_and_masks_query_values",
        "harness.test_runner.RedactionTests."
        "test_sanitize_detail_does_not_pass_a_body_through",
        "harness.test_runner.RedactionTests."
        "test_an_http_error_body_is_never_persisted",
    ),),
    "write-boundary": (unit(
        "harness.test_runner.SlugTests.test_traversal_is_refused",
        "harness.test_runner.SlugTests.test_a_plain_slug_is_accepted",
        "harness.test_runner.SlugTests.test_product_dir_stays_under_products",
        "harness.test_runner.SlugTests."
        "test_guard_output_refuses_outside_products",
        "harness.test_runner.SlugTests."
        "test_guard_output_refuses_a_traversal_that_resolves_out",
        "harness.test_runner.RunTaskTests."
        "test_a_traversal_product_never_reaches_a_model_call",
    ),),
    "compile-all": (probe("compile-all"),),
    "full-suite": (probe("full-suite", timeout=1800),),
    "ci-runtime": (probe("ci-covers-runtime"),),
    "deletable-harness": (probe("deletable-harness"),),
    "mutation-gates": (probe("mutation-checks", timeout=1800),),
    "golden-path": (probe("golden-path"),),
    "regulated-example": (
        Step(("python3", "lint.py",
              "modules/regulated/examples/dispute-summary/PRD.md")),),
    "independent-review": (
        unit(*REVIEW_TESTS),
        Step(("python3", "tools/review_gate.py")),
    ),
}


def known(verifier_id):
    return verifier_id in REGISTRY
