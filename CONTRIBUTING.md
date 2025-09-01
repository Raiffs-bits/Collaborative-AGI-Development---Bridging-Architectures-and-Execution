
# Contributing

Thanks for contributing to the AGI Governance Benchmark!

## Branching & PRs
- Create feature branches from `main`.
- Add a clear PR title and fill in the PR template.
- Keep diffs focused — avoid committing generated artifacts unless necessary.

## Code Style
- Python: PEP8. Prefer type hints and docstrings.
- TypeScript: strict types, small modules.

## Tests / CI
- Ensure `run_harness.py` and `score_results.py` run locally before PR.
- CI will execute a short demo run against `tasks.jsonl` and publish artifacts.

## Structure (proposed)
- `tasks.jsonl` — tasks
- `trace_schema.yaml` — trace schema
- `run_harness.py` / `run_harness.ts` — reference harness
- `score_results.py` — scoring
- `eval_utils.py`, `fairness_metrics.py`, `security_utils.py`, `visualization_utils.py` — utilities
- `error_recovery_handler.py` — recovery orchestration
- `docs/` — executive summaries, partner readmes
- `.github/workflows/` — CI

## Large Files
- Avoid adding large models/binaries to the repo. Use release artifacts if needed.

## License
- MIT. By contributing you agree to license your contributions under MIT.
