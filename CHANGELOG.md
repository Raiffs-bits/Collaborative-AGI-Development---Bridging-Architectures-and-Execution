
# Changelog

## v1.1 (2025-08-31)
- Added fairness metrics (fairness_metrics.py).
- Added security utilities (security_utils.py).
- Added visualization utilities (visualization_utils.py).
- Added error recovery categorization (error_recovery.py).
- Updated README with new usage examples.

## v1.0 (2025-08-30)
- Initial release with tasks.jsonl, schema, harnesses, eval utils, and scoring scripts.

## v1.2 (2025-08-31)
- Added `error_recovery_handler.py` with pluggable ModelClient, deterministic RNG, and optional fairness + encryption.
- Added `config_recovery.yaml` and `run_harness_recovery.py` demo runner.
- Added `README_RECOVERY.md` documentation.
- Collected recovery distribution in `recovery_stats.json`.
