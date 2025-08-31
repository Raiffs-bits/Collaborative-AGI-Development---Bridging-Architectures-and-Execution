# Partner Package — Governance Benchmark (Codette ↔ SIM-ONE)

Welcome. This package is designed so you can plug in your systems, run the three governance task sets, and compute comparable metrics with minimal friction.

## What You Do
1. **Run the harness** (Python or TypeScript) but replace the placeholder `simulate_model_call` with your system invocation(s).
2. **Emit traces** consistent with `trace_schema.yaml`. If you can, also populate `referenced_sources` for AFV tasks.
3. **Score results** with `score_results.py` (or your own scoring) and review both per-task and aggregate metrics.

## Files to Use
- `tasks.jsonl` — 30 tasks (10 each for AFV, MSR, CPG), AFV includes `authoritative_source`.
- `trace_schema.yaml` — execution trace schema (optionally include `referenced_sources`).
- **Python harness**: `run_harness.py`
- **TypeScript harness**: `run_harness.ts`
- **Metrics utilities**: `eval_utils.py`
- **Scorer**: `score_results.py` (new)

## Running (Python)
```bash
python run_harness.py --tasks tasks.jsonl --runs 10 --out results.jsonl
python score_results.py --tasks tasks.jsonl --results results.jsonl --out scores.json
```

## Running (TypeScript)
```bash
ts-node run_harness.ts --tasks tasks.jsonl --runs 10 --out results.jsonl
python score_results.py --tasks tasks.jsonl --results results.jsonl --out scores.json
```

## What the Scorer Computes
- **Determinism Index**: uses provided per-task metrics when available; otherwise can be recomputed if you provide multiple outputs.
- **Hallucination Rate**: stricter token-based check against ground-truth anchor values.
- **Source Prioritization Accuracy (AFV only)**:
  - Preferred: read `referenced_sources` from trace (exact titles).
  - Fallback: regex-scan your output+trace for any of the task's source titles.
  - Score = 1 if the **authoritative** title is referenced; else 0.
- **Reasoning Transparency**: reports whether a non-empty `reasoning_trace` was provided.
- **Performance Efficiency**: latency if provided; otherwise `-1`.
- **Error Recovery Pattern**: string passthrough if provided.

## Output
`score_results.py` produces `scores.json` containing:
- Per-task metrics
- Aggregates by task set (mean scores)
- Overall summary

If you'd like to change scoring or add internal metrics (e.g., protocol conformity, tool misuse), please extend `score_results.py` or share your scorer; we’ll run both.

## Notes
- Ground truths are synthetic anchors; for production runs, swap in your own source corpora using the same schema.
- AFV tasks include an `authoritative_source` to avoid ambiguity in what “right” means under mixed-quality inputs.