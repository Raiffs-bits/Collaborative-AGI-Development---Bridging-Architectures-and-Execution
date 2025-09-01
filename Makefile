
.PHONY: demo score ci validate

demo:
	python run_harness.py --tasks tasks.jsonl --runs 10 --out results.jsonl

score:
	python score_results.py --tasks tasks.jsonl --results results.jsonl --out scores.json

recovery:
	python run_harness_recovery.py --tasks tasks.jsonl --simulate_errors --out results_recovery.jsonl

validate:
	./scripts/validate_tasks.py tasks.jsonl

ci: demo score
