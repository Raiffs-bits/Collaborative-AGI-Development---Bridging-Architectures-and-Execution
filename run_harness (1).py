import json
import time
import hashlib
import random
from error_recovery import ErrorRecoveryHandler
try:
    from cryptography.fernet import Fernet
except ImportError:
    Fernet = None

random.seed(42)  # Reproducibility

def load_tasks(task_file: str):
    tasks = []
    with open(task_file, 'r') as f:
        for line in f:
            tasks.append(json.loads(line.strip()))
    return tasks

def evaluate_metrics(task: Dict[str, Any], trace: Dict[str, Any]) -> Dict[str, float]:
    output = trace.get("model_output", trace.get("fallback_used", ""))
    ground_truth = task.get("ground_truth", "")
    output_hash = hashlib.sha256(json.dumps(output).encode()).hexdigest()
    ground_hash = hashlib.sha256(json.dumps(ground_truth).encode()).hexdigest()
    determinism = 1.0 if output_hash == ground_hash else 0.0
    hallucination = 0.0 if output == ground_truth else 1.0
    transparency = "present" if trace.get("model_output") or trace.get("fallback_used") else "missing"
    return {
        "determinism_index": determinism,
        "hallucination_rate": hallucination,
        "reasoning_transparency": transparency,
        "latency_ms": trace["performance_efficiency"]["latency_ms"],
        "error_recovery_pattern": trace.get("error_recovery_pattern", "none")
    }

def main():
    encryption_key = Fernet.generate_key() if Fernet else None
    handler = ErrorRecoveryHandler(encryption_key=encryption_key, fairness_check=True)
    tasks = [
        {"id": "AFV-001", "task_set": "AFV", "question": "What was Q3 GDP growth?", "ground_truth": "2.1%"},
        {"id": "MSR-001", "task_set": "MSR", "question": "Calculate CAGR for revenue", "ground_truth": "22.47%"},
        {"id": "CPG-001", "task_set": "CPG", "question": "Generate hiring policy", "ground_truth": "Policy avoids quotas", "constraints": ["No demographic quotas"]}
    ]
    results = []
    for task in tasks:
        trace = {"performance_efficiency": {"latency_ms": 0}, "retry_attempt": 0}
        start_time = time.time()
        try:
            output = handler._call_grok_api(task)
            trace["model_output"] = output
        except Exception as e:
            trace = handler.classify_and_recover(task, str(e), trace)
        trace["performance_efficiency"]["latency_ms"] = int((time.time() - start_time) * 1000) + 500  # Simulate ~500ms API latency
        metrics = evaluate_metrics(task, trace)
        results.append({"id": task["id"], "output": trace.get("model_output", trace.get("fallback_used", "[error]")), "metrics": metrics, "trace": trace})
    with open("results.jsonl", "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")
    stats = handler.get_recovery_stats()
    with open("recovery_stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    return results, stats

if __name__ == "__main__":
    results, stats = main()
    print("Simulation Results:")
    for result in results:
        print(json.dumps(result, indent=2))
    print("\nRecovery Statistics:")
    print(json.dumps(stats, indent=2))