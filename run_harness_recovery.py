
# run_harness_recovery.py
import json, time, argparse
from pathlib import Path
from typing import Dict, Any
from error_recovery_handler import ErrorRecoveryHandler, DummyModelClient

def load_tasks(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def simulate_with_recovery(task: Dict[str, Any], handler: ErrorRecoveryHandler) -> Dict[str, Any]:
    trace = {"performance_efficiency": {"latency_ms": 0}}
    start = time.time()
    try:
        # Initial attempt
        output = handler.model_client.call(task)
        trace["model_output"] = output
        trace["performance_efficiency"]["latency_ms"] = int((time.time() - start) * 1000)
        trace["error_recovery_pattern"] = "none"
        trace["recovery_outcome"] = "N/A"
        return trace
    except Exception as e:
        trace["exception"] = type(e).__name__
        trace["performance_efficiency"]["latency_ms"] = int((time.time() - start) * 1000)
        return handler.classify_and_recover(task, type(e).__name__, trace)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="tasks.jsonl")
    ap.add_argument("--out", default="results_recovery.jsonl")
    ap.add_argument("--simulate_errors", action="store_true")
    args = ap.parse_args()

    # Simulate failures for a subset by id
    error_map = {}
    if args.simulate_errors:
        error_map = {"MSR-001": "RuntimeError", "CPG-001": "ConstraintViolation"}

    handler = ErrorRecoveryHandler(model_client=DummyModelClient(error_map=error_map), rng_seed=42, fairness_check=True)

    with open(args.out, "w", encoding="utf-8") as outf:
        for task in load_tasks(args.tasks):
            if task.get("id") in ("AFV-001","MSR-001","CPG-001"):
                trace = simulate_with_recovery(task, handler)
                record = {"id": task["id"], "task_set": task["task_set"], "trace": trace, "last_output": trace.get("model_output", "")}
                outf.write(json.dumps(record) + "\n")

    stats = handler.get_recovery_stats()
    Path("recovery_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print("Wrote", args.out, "and recovery_stats.json")

if __name__ == "__main__":
    main()
