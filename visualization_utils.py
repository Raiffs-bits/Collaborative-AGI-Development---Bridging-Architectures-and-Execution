
# visualization_utils.py
# Simple visualization utilities for benchmark metrics

import json
import matplotlib.pyplot as plt

def scatter_hallucination_vs_determinism(scores_file: str):
    with open(scores_file, 'r') as f:
        data = json.load(f)
    xs, ys = [], []
    for t in data.get('per_task', []):
        m = t['metrics']
        xs.append(m.get('hallucination_rate', 0))
        ys.append(m.get('determinism_index', 0))
    plt.scatter(xs, ys)
    plt.xlabel('Hallucination Rate')
    plt.ylabel('Determinism Index')
    plt.title('Hallucination vs Determinism')
    plt.show()

def bar_latency(scores_file: str):
    with open(scores_file, 'r') as f:
        data = json.load(f)
    task_sets = {}
    for t in data.get('per_task', []):
        ts = t['task_set']
        lat = t['metrics'].get('performance_efficiency', {}).get('latency_ms', None)
        if lat is not None:
            task_sets.setdefault(ts, []).append(lat)
    avg = {k: sum(v)/len(v) for k,v in task_sets.items() if v}
    plt.bar(avg.keys(), avg.values())
    plt.ylabel('Average Latency (ms)')
    plt.title('Latency by Task Set')
    plt.show()
