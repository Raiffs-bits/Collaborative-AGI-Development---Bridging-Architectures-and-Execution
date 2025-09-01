
# Executive Summary — AGI Governance Benchmark

**What it is**: A portable, reproducible benchmark for evaluating AI reliability across:
- Adversarial Fact Verification (AFV)
- Multi-Step Tool-Augmented Reasoning (MSR)
- Constrained Policy Generation (CPG)

**Why it matters**: It measures determinism, hallucination, source selection, constraint adherence, fairness, and recovery — the pillars of governed cognition.

**What’s included**:
- Tasks (`tasks.jsonl`), Trace schema (`trace_schema.yaml`)
- Harnesses (Python/TS), Scorer (`score_results.py`)
- Utilities (evaluation, fairness, security, recovery, visualization)
- CI workflow that runs a short demo and publishes artifacts

**What’s new (v1.2)**:
- Error recovery orchestrator with retry/fallback/escalate/safe-fail
- Optional fairness proxy check and encrypted recovery logs
- Partner-ready docs and demo artifacts

**How to use**:
1. Run the harness: `python run_harness.py --tasks tasks.jsonl --runs 10 --out results.jsonl`
2. Score: `python score_results.py --tasks tasks.jsonl --results results.jsonl --out scores.json`
3. (Optional) Recovery demo: `python run_harness_recovery.py --tasks tasks.jsonl --simulate_errors`
4. Review CI artifacts for a quick sanity check

**Roadmap**:
- Graded hallucination metric by default
- Expanded task bank with multilingual/noisy/contradictory cases
- Dashboard visualizations and fairness auditing hooks
