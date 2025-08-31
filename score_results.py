import argparse, json, re
from pathlib import Path
from statistics import mean

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def build_task_map(tasks):
    return {t["id"]: t for t in tasks}

def find_titles_in_text(titles, text):
    hits = []
    for t in titles:
        # Exact title mention (case-insensitive), escape regex specials
        pat = re.escape(t)
        if re.search(pat, text, flags=re.IGNORECASE):
            hits.append(t)
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--results", required=True)
    ap.add_argument("--out", default="scores.json")
    args = ap.parse_args()

    tasks = load_jsonl(args.tasks)
    results = load_jsonl(args.results)
    task_map = build_task_map(tasks)

    per_task = []
    by_set = {}

    for r in results:
        tid = r.get("id")
        t = task_map.get(tid, {})
        tset = r.get("task_set", t.get("task_set", "UNKNOWN"))
        metrics = r.get("metrics", {})
        last_output = r.get("last_output", r.get("output", ""))
        # Try to retrieve a reasoning trace if present
        trace = r.get("trace", "")
        # Some runners may store trace under metrics; leave as-is if missing

        spa = None
        if tset == "Adversarial Fact Verification":
            titles = [s["title"] for s in t.get("sources", [])]
            auth = t.get("authoritative_source", "")
            # Preferred: referenced_sources array (exact titles)
            referenced = r.get("referenced_sources") or []
            # Fallback: parse from output+trace
            if not referenced:
                referenced = find_titles_in_text(titles, (last_output or "") + " " + (trace or ""))
            spa = 1.0 if auth and (auth in referenced) else 0.0
            metrics["source_prioritization_accuracy"] = spa

        # Transparency proxy
        if "reasoning_transparency" not in metrics:
            metrics["reasoning_transparency"] = "present" if trace else "missing"

        per_task.append({
            "id": tid,
            "task_set": tset,
            "metrics": metrics
        })

        by_set.setdefault(tset, []).append(metrics)

    # Aggregates
    summary = {}
    def agg_mean(items, key):
        vals = [m.get(key) for m in items if isinstance(m.get(key), (int, float))]
        return mean(vals) if vals else None

    for tset, ms in by_set.items():
        summary[tset] = {
            "avg_determinism_index": agg_mean(ms, "determinism_index"),
            "avg_hallucination_rate": agg_mean(ms, "hallucination_rate"),
            "avg_source_prioritization_accuracy": agg_mean(ms, "source_prioritization_accuracy"),
            "avg_latency_ms": agg_mean([m.get("performance_efficiency", {}) for m in ms], "latency_ms")
        }

    out = {"per_task": per_task, "summary": summary}
    Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()