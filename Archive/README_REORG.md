
# Repository Reorg Plan

This repo currently includes multiple *update variants* (e.g., `eval_utilsUpdate.py`, `fairness_metrics2.py`, `tasksUpdate.jsonl`, `trace_schemaUpdate.yaml`). To reduce confusion:

## Keep (canonical)
- `tasks.jsonl`
- `trace_schema.yaml`
- `run_harness.py`, `run_harness.ts`, `run_harness_recovery.py`
- `score_results.py`, `eval_utils.py`
- `error_recovery_handler.py`
- `fairness_metrics.py`, `security_utils.py`, `visualization_utils.py`
- `README.md`, `README_UPDATED.md`, `README_RECOVERY.md`, `PARTNER_README.md`
- `CHANGELOG.md`

## Remove or archive
- `*Update*.py`, `*Update*.ts`, `tasksUpdate.jsonl`, `trace_schemaUpdate.yaml`, `trace_schemaBC.yaml`, duplicates like `fairness_metrics2.py`, `security_utils2.py`, `error_recovery2.py`.
- If content differs, merge improvements back into the canonical files first.

## Structure (suggested)
- `/docs` — executive summaries & partner docs
- `/scripts` — validation and helper scripts
- `/.github/workflows` — CI
- root — tasks, schema, harnesses, scorers, core utilities

## Next steps
1. Run `scripts/validate_tasks.py tasks.jsonl` to ensure integrity.
2. Merge any improvements from `*Update*` files into canonical ones.
3. Delete superseded variants in a single PR titled **Repo cleanup: consolidate duplicates**.
