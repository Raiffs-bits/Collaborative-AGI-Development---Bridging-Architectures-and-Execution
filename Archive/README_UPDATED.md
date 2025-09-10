
# AGI Governance Benchmark — Updated Release

This benchmark suite evaluates AI systems across three domains:
- **Adversarial Fact Verification (AFV)**
- **Multi-Step Tool-Augmented Reasoning (MSR)**
- **Constrained Policy Generation (CPG)**

## What's New
- **Fairness Metrics**: Added `fairness_metrics.py` for demographic parity, equal opportunity, and disparate impact scoring (CPG).
- **Security Utilities**: Added `security_utils.py` for AES-256 encryption/decryption of task and trace files.
- **Visualization**: Added `visualization_utils.py` for scatter and bar charts (hallucination vs. determinism, latency by set).
- **Error Recovery**: Added `error_recovery.py` to classify recovery behavior into `retry`, `fallback`, `escalate`, `safe-fail`.

## File Overview
- `tasks.jsonl` — Benchmark tasks (30 total)
- `trace_schema.yaml` — Execution trace schema
- `run_harness.py` / `run_harness.ts` — Reference harnesses
- `eval_utils.py` — Core evaluation utilities
- `score_results.py` — Scoring engine
- `fairness_metrics.py` — Fairness metrics
- `security_utils.py` — Encryption/decryption
- `visualization_utils.py` — Quick metric plots
- `error_recovery.py` — Recovery pattern classification

## Usage Examples

### Run + Score
```bash
python run_harness.py --tasks tasks.jsonl --runs 10 --out results.jsonl
python score_results.py --tasks tasks.jsonl --results results.jsonl --out scores.json
```

### Visualize
```python
from visualization_utils import scatter_hallucination_vs_determinism, bar_latency
scatter_hallucination_vs_determinism('scores.json')
bar_latency('scores.json')
```

### Fairness Audit (CPG)
```python
from fairness_metrics import demographic_parity, equal_opportunity, disparate_impact
selected = [1,0,1,1]
groups = ['A','A','B','B']
print(demographic_parity(selected, groups))
```

### Security
```python
from security_utils import generate_key, encrypt_file, decrypt_file
key = generate_key()
encrypt_file(key, 'tasks.jsonl', 'tasks.enc')
decrypt_file(key, 'tasks.enc', 'tasks_dec.jsonl')
```

## Changelog
See `CHANGELOG.md` for version history.
