import json
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
    # Average pairwise Jaccard * Levenshtein ratio
    if len(outputs) < 2:
        return 1.0
    pairs = 0
    acc = 0.0
    for i in range(len(outputs)):
        for j in range(i+1, len(outputs)):
            acc += 0.5 * jaccard(outputs[i], outputs[j]) + 0.5 * levenshtein_ratio(outputs[i], outputs[j])
            pairs += 1
    return acc / pairs if pairs else 1.0

def hallucination_rate(output: str, ground_truth) -> float:
    # Simplistic: if GT string/object content isn't referenced, flag as hallucination (to be replaced by stricter check)
    if isinstance(ground_truth, dict):
        gt_str = json.dumps(ground_truth)
    else:
        gt_str = str(ground_truth)
    return 0.0 if gt_str.strip() and gt_str.strip() in output else 1.0

def source_prioritization_accuracy(chosen_source_title: str, authoritative_titles: List[str]) -> float:
    return 1.0 if chosen_source_title in authoritative_titles else 0.0