
# fairness_metrics.py
# Simple fairness metric stubs for Constrained Policy Generation (CPG) tasks

from typing import List, Dict

def demographic_parity(selected: List[int], groups: List[str]) -> float:
    """Compute demographic parity: average selection rate across groups."""
    rates = {}
    for sel, g in zip(selected, groups):
        rates.setdefault(g, []).append(sel)
    group_rates = [sum(v)/len(v) for v in rates.values()]
    return min(group_rates) / max(group_rates) if max(group_rates) > 0 else 0.0

def equal_opportunity(true_labels: List[int], selected: List[int], groups: List[str]) -> Dict[str, float]:
    """Compute TPR by group."""
    tprs = {}
    for g in set(groups):
        tp = sum(1 for t,s,gg in zip(true_labels, selected, groups) if gg==g and t==1 and s==1)
        fn = sum(1 for t,s,gg in zip(true_labels, selected, groups) if gg==g and t==1 and s==0)
        denom = tp+fn
        tprs[g] = tp/denom if denom>0 else 0.0
    return tprs

def disparate_impact(selected: List[int], groups: List[str]) -> float:
    """Compute disparate impact ratio (80% rule)."""
    rates = {}
    for sel, g in zip(selected, groups):
        rates.setdefault(g, []).append(sel)
    group_rates = [sum(v)/len(v) for v in rates.values()]
    if len(group_rates) < 2: return 1.0
    return min(group_rates) / max(group_rates)
