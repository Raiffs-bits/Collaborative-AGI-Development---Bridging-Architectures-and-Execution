# Governance Benchmark Package (Codette ↔ SIM-ONE)

This package provides a **30-example** benchmark across three governance-first task sets, a **trace schema**, a **reproducible harness**, and **evaluation utilities**. It is designed to be fine‑tuned or extended by partner teams. Final testing can be executed with their runners without modifying the task pack.

## Contents
- `tasks.jsonl` — 30 tasks (10 per set)
- `trace_schema.yaml` — execution trace schema for logs and tools
- `eval_utils.py` — metric primitives (determinism, hallucination, source prioritization)
- `run_harness.py` — reference runner (replace `simulate_model_call` with your system)
- `README.md` — this file

## Task Sets
1. **Adversarial Fact Verification (AFV)** — stress-tests truth anchoring with mixed-reliability sources.
2. **Multi-Step Tool-Augmented Reasoning (MSR)** — evaluates deterministic execution with structured inputs.
3. **Constrained Policy Generation (CPG)** — tests ethical adherence and recovery under edge constraints.

## Metrics
- **Determinism Index** — stability across identical runs
- **Hallucination Rate** — unsupported claim indicator (replace with stricter checker if needed)
- **Source Prioritization Accuracy** — whether authoritative sources were selected (for AFV tasks)
- **Reasoning Transparency** — presence/quality of intermediate trace and tool calls
- **Performance Efficiency** — latency & cost
- **Error Recovery Pattern** — behavior on near-violations or ambiguity

## Usage
```bash
python run_harness.py --tasks tasks.jsonl --runs 10 --out results.jsonl
```

Replace the placeholder `simulate_model_call` with calls into your system(s), and emit traces consistent with `trace_schema.yaml`.

## Notes
- Ground truths here are **anchors for evaluation**, not real-world claims. For production comparisons, swap in live, cited sources.
- The package is intentionally minimal and inspectable. Extend as needed for your internal evaluation stack.