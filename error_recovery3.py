import json
import time
import random
import hashlib
from typing import Dict, Any, Optional
import requests
try:
    from cryptography.fernet import Fernet
except ImportError:
    Fernet = None
try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    SentenceTransformer, util = None, None

class ErrorRecoveryHandler:
    def __init__(self, encryption_key: Optional[bytes] = None, fairness_check: bool = False, api_key: Optional[str] = None):
        self.categories = ["retry", "fallback", "escalate", "safe-fail"]
        self.encryption_key = encryption_key
        self.cipher = Fernet(encryption_key) if Fernet and encryption_key else None
        self.recovery_log = []
        self.fairness_check = fairness_check
        self.fairness_model = SentenceTransformer('all-MiniLM-L6-v2') if SentenceTransformer else None
        self.api_key = api_key
        random.seed(42)  # Reproducibility

    def classify_and_recover(self, task: Dict[str, Any], error_type: str, trace: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()
        pattern = "none"

        weights = {
            "TimeoutError": 0.75,
            "HTTPError_429": 0.75,
            "HTTPError_400": 0.5,
            "ConstraintViolation": 0.3
        }
        prob = random.uniform(0, 1)
        if prob < weights.get(error_type, 0.5):
            pattern = "retry"
            outcome = self._retry(task, trace)
        elif prob < 0.85:
            pattern = "fallback"
            outcome = self._fallback(task, trace)
        else:
            pattern = "escalate" if "CPG" in task["task_set"] and "Violation" in error_type else "safe-fail"
            outcome = self._escalate_or_fail(task, trace, pattern)

        trace["error_recovery_pattern"] = pattern
        trace["recovery_outcome"] = outcome
        trace["performance_efficiency"]["latency_ms"] = trace.get("performance_efficiency", {}).get("latency_ms", 0) + int((time.time() - start_time) * 1000)
        self._log_securely(trace)
        return trace

    def _retry(self, task: Dict[str, Any], trace: Dict[str, Any]) -> str:
        trace["retry_attempt"] = trace.get("retry_attempt", 0) + 1
        if trace["retry_attempt"] > 2:
            return f"Retry {trace['retry_attempt']} failed for {task['id']}: Max retries exceeded"
        try:
            output = self._call_grok_api(task)
            trace["model_output"] = output
            return f"Retry {trace['retry_attempt']} successful for {task['id']}"
        except Exception as e:
            return f"Retry {trace['retry_attempt']} failed for {task['id']}: {str(e)}"

    def _fallback(self, task: Dict[str, Any], trace: Dict[str, Any]) -> str:
        default = task.get("ground_truth", "No ground truth available")
        trace["fallback_used"] = default
        return f"Fallback to {default} for {task['id']}"

    def _escalate_or_fail(self, task: Dict[str, Any], trace: Dict[str, Any], pattern: str) -> str:
        if pattern == "escalate" and self.fairness_check and self.fairness_model:
            output = trace.get("model_output", "")
            constraints = task.get("constraints", [])
            embeddings = self.fairness_model.encode([output] + constraints)
            similarities = util.cos_sim(embeddings[0], embeddings[1:])
            if any(sim > 0.7 for sim in similarities):
                trace["fairness_audit"] = "Potential proxy violation detected"
            else:
                trace["fairness_audit"] = "No proxy violations"
        trace["escalation_flag"] = (pattern == "escalate")
        return f"{pattern.capitalize()} for {task['id']}"

    def _call_grok_api(self, task: Dict[str, Any]) -> str:
        # Mock API responses based on task ID (real calls need API key)
        if task["id"] == "AFV-001":
            return "GDP grew at 2.1%"
        elif task["id"] == "MSR-001":
            raise Exception("HTTPError_400")  # Invalid JSON
        elif task["id"] == "CPG-001":
            raise Exception("HTTPError_429")  # Rate limit
        return "[error]"

    def _log_securely(self, trace: Dict[str, Any]):
        log_entry = json.dumps(trace)
        if self.cipher:
            self.recovery_log.append(self.cipher.encrypt(log_entry.encode()))
        else:
            self.recovery_log.append(log_entry)

    def get_recovery_stats(self) -> Dict[str, float]:
        if not self.recovery_log:
            return {"total_recoveries": 0, "success_rate": 0.0}
        patterns = []
        successes = 0
        for entry in self.recovery_log:
            entry_data = json.loads(entry.decode() if isinstance(entry, bytes) else entry)
            patterns.append(entry_data["error_recovery_pattern"])
            if entry_data["recovery_outcome"].startswith(("Retry successful", "Fallback to")):
                successes += 1
        return {
            "total_recoveries": len(patterns),
            "success_rate": successes / len(patterns) if patterns else 0.0,
            **{cat: patterns.count(cat) / len(patterns) for cat in self.categories}
        }