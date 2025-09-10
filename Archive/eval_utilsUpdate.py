import json, re
from typing import List, Dict, Any
from difflib import SequenceMatcher

def jaccard(a: str, b: str) -> float:
    sa, sb = set(a.split()), set(b.split())
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / max(1, len(sa | sb))

def levenshtein_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def determinism_index(outputs: List[str]) -> float:
    if len(outputs) < 2:
        return 1.0
    pairs, acc = 0, 0.0
    for i in range(len(outputs)):
        for j in range(i+1, len(outputs)):
            acc += 0.5 * jaccard(outputs[i], outputs[j]) + 0.5 * levenshtein_ratio(outputs[i], outputs[j])
            pairs += 1
    return acc / pairs if pairs else 1.0

def hallucination_rate(output: str, ground_truth) -> float:
    # Tokenize ground truth values and check if present in output (stricter than substring check)
    gt_tokens = []
    if isinstance(ground_truth, dict):
        gt_tokens = re.findall(r"[A-Za-z0-9\.\%]+", json.dumps(ground_truth))
    else:
        gt_tokens = re.findall(r"[A-Za-z0-9\.\%]+", str(ground_truth))
    missing = [tok for tok in gt_tokens if tok not in output]
    return 0.0 if not missing else 1.0

def source_prioritization_accuracy(referenced_sources: List[str], authoritative_title: str) -> float:
    return 1.0 if authoritative_title in referenced_sources else 0.0