Governance Benchmark Package (Codette ↔ SIM-ONE) — Enhanced Edition

This repository provides a governance-first benchmark for evaluating AI systems, with a focus on truth anchoring, ethical resilience, determinism, and transparency.
It includes 30 tasks across three sets (Adversarial Fact Verification, Multi-Step Tool-Augmented Reasoning, Constrained Policy Generation), with structured traces, metrics, and harnesses in both Python and TypeScript.

Transparency & Development History

This repo intentionally preserves earlier iterations (see the /archive/ folder) to document the full development trail.
Governance benchmarking requires not only results, but proof of how they were reached.
Dead-ends, fixes, recovery attempts, and experimental variants are logged here for reproducibility and auditability.

Canonical files for current usage:

run_harness.py (Python reference runner)

run_harness.ts (TypeScript reference runner)

eval_utils.py (evaluation utilities, stricter hallucination + source prioritization)

error_recovery_handler.py (standard error recovery logic)

fairness_metrics.py (fairness and bias scoring utilities)

tasks.jsonl (task set definitions)

trace_schema.yaml (execution trace schema)

Historical versions are archived under /archive/ for transparency.

Contents

tasks.jsonl — 30 tasks (10 per set), with authoritative_source in AFV tasks for source prioritization

trace_schema.yaml — execution trace schema

eval_utils.py — stricter hallucination checker, explicit source prioritization metric

run_harness.py — Python runner (replace simulate_model_call with your system)

run_harness.ts — TypeScript runner

results_demo.jsonl — sample baseline run (deterministic stub model)

Codette_Governance_Benchmark_Scores.csv — sample scores

fairness_metrics.py — fairness/bias checks

Task Sets
1. Adversarial Fact Verification (AFV)

Stress-tests truth anchoring with mixed-reliability sources.

Each task includes an authoritative_source field identifying the correct reference.

2. Multi-Step Tool-Augmented Reasoning (MSR)

Evaluates deterministic execution with structured inputs and calculations.

3. Constrained Policy Generation (CPG)

Tests ethical adherence and recovery under explicit red-lines.

Metrics

Determinism Index — stability across identical runs (% identical outputs).

Hallucination Rate (strict) — requires ground truth tokens in outputs.

Source Prioritization Accuracy — AFV: did the system reference the authoritative source?

Reasoning Transparency — presence and clarity of intermediate steps.

Performance Efficiency — latency and cost per task.

Error Recovery Pattern — behavior on near-violations or ambiguous inputs.

Fairness Metrics — bias and distribution checks (fairness_metrics.py).

Usage
Python
python run_harness.py --tasks tasks.jsonl --runs 10 --out results.jsonl
python score_results.py results.jsonl

TypeScript
ts-node run_harness.ts --tasks tasks.jsonl --runs 10 --out results.jsonl


Replace placeholder calls (simulate_model_call) with actual system invocations.

Changelog Highlights

Added authoritative_source in AFV tasks

Strengthened hallucination checker (token-level)

Added run_harness.ts for Node.js/TypeScript

Merged Enhanced instructions into this unified README

Added fairness_metrics.py

Full details: see CHANGELOG.md
.

Notes

Ground truths are synthetic anchors. Replace/augment with live sources for production.

The benchmark is deliberately small (30 items) for reproducibility. Extend as needed.

Historical versions are preserved in /archive/ for transparency.

Citation
@misc{codette_governance_benchmark,
  title        = {Governance Benchmark Package (Codette ↔ SIM-ONE)},
  year         = 2025,
  publisher    = {Raiff's Bits LLC},
  url          = {https://github.com/Raiffs-bits/Collaborative-AGI-Development---Bridging-Architectures-and-Execution}
}