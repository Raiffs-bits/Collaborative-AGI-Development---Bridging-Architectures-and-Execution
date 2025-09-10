# Governance Benchmark Package (Codette ↔ SIM-ONE) — Enhanced Edition

This is an updated release of the governance-first benchmark, incorporating stricter evaluation guidance, source-tagging for fact verification, and cross-language harness support.

## Contents
- `tasks.jsonl` — 30 tasks (10 per set), now with **authoritative_source field** in Adversarial Fact Verification tasks for source prioritization scoring
- `trace_schema.yaml` — unchanged execution trace schema
- `eval_utils.py` — updated with stricter hallucination checker and explicit source prioritization metric
- `run_harness.py` — reference Python runner (replace `simulate_model_call` with your system)
- `run_harness.ts` — TypeScript reference harness (new)
- `README.md` — previous version
- `README_ENHANCED.md` — this file (enhanced instructions + changelog)

## Task Sets
1. **Adversarial Fact Verification (AFV)**  
   - Stress-tests truth anchoring with mixed-reliability sources.  
   - Each task now includes an `authoritative_source` field identifying the correct reference title.

2. **Multi-Step Tool-Augmented Reasoning (MSR)**  
   - Evaluates deterministic execution with structured inputs and calculations.  

3. **Constrained Policy Generation (CPG)**  
   - Tests ethical adherence and recovery under explicit red-lines.

## Metrics
- **Determinism Index** — stability across identical runs
- **Hallucination Rate (stricter)** — checks unsupported claims by comparing output spans against ground truth tokens/values
- **Source Prioritization Accuracy** — AFV tasks: was the authoritative source selected/referenced?
- **Reasoning Transparency** — presence/quality of intermediate steps
- **Performance Efficiency** — latency & cost
- **Error Recovery Pattern** — behavior on near-violations or ambiguity

## Usage (Python)
```bash
python run_harness.py --tasks tasks.jsonl --runs 10 --out results.jsonl
```

## Usage (TypeScript)
```bash
ts-node run_harness.ts --tasks tasks.jsonl --runs 10 --out results.jsonl
```

Replace placeholder calls in either harness with actual system invocations.

## Changelog
- **Added authoritative_source field** in AFV tasks to explicitly mark the ground-truth source for prioritization metrics.
- **Strengthened hallucination checker** in `eval_utils.py` to tokenize ground truth values and require their presence in outputs (not just string match).
- **Added run_harness.ts** — a TypeScript reference harness for teams preferring Node.js/TS evaluation stacks.
- **README_ENHANCED.md created** — includes expanded evaluation guidance, cross-language harness support, and changelog.

## Notes
- Ground truths are **synthetic anchors** for evaluation. Replace or augment with live sources for production use.
- The benchmark is deliberately small (30 items) for reproducibility and fine-tuning. Extend as needed for more coverage.