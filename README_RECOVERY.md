
# Error Recovery Orchestration — Guide

This module introduces **pluggable error recovery** for your benchmark runs:
- Probabilistic choice between `retry`, `fallback`, `escalate`, `safe-fail`
- Optional **encryption** of recovery logs (Fernet)
- Optional **fairness proxy detection** (Sentence-Transformers)
- Pluggable **ModelClient** interface (Grok/OpenAI/etc.)

## Files
- `error_recovery_handler.py` — main orchestration logic
- `config_recovery.yaml` — tunable thresholds and retry limits
- `run_harness_recovery.py` — reference runner wiring the handler
- `recovery_stats.json` — summary distribution and success rate

## Quickstart
```bash
# simulate recovery on 3 demo tasks (AFV-001, MSR-001, CPG-001)
python run_harness_recovery.py --tasks tasks.jsonl --simulate_errors --out results_recovery.jsonl

# view stats
cat recovery_stats.json
```

## Plug your own model
Implement `ModelClient.call(self, task) -> str` and pass it into `ErrorRecoveryHandler(model_client=YourClient())`.

## Fairness Auditing
Enable with `fairness_check=True`. If you pass CPG constraints, the handler will run a proxy-similarity check and annotate the trace with a fairness audit note.

## Encryption
Provide a Fernet key to encrypt recovery logs at rest:
```python
from cryptography.fernet import Fernet
from error_recovery_handler import ErrorRecoveryHandler

key = Fernet.generate_key()
handler = ErrorRecoveryHandler(encryption_key=key)
```

## Notes
- Defaults are deterministic with `rng_seed` for reproducible recovery choices.
- For full-benchmark runs, integrate the handler into your main harness and emit traces consistent with `trace_schema.yaml`.
