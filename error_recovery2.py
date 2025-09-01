
# error_recovery.py
# Categorize and log error recovery patterns

def classify_recovery(log: str) -> str:
    log_lower = log.lower()
    if 'retry' in log_lower:
        return 'retry'
    if 'fallback' in log_lower:
        return 'fallback'
    if 'escalate' in log_lower:
        return 'escalate'
    if 'abort' in log_lower or 'safe-fail' in log_lower:
        return 'safe-fail'
    return 'none'
