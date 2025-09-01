
#!/usr/bin/env python3
import json, sys

def main(path: str):
    ok = True
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            obj = json.loads(line)
            # Basic checks
            for k in ('task_set','id'):
                if k not in obj:
                    print(f'[L{i}] missing key: {k}', file=sys.stderr)
                    ok = False
            if obj.get('task_set') == 'Adversarial Fact Verification':
                if 'authoritative_source' not in obj:
                    print(f'[L{i}] AFV missing authoritative_source', file=sys.stderr)
                    ok = False
            if obj.get('task_set') == 'Multi-Step Tool-Augmented Reasoning':
                if 'filings' not in obj or 'ground_truth' not in obj:
                    print(f'[L{i}] MSR missing filings/ground_truth', file=sys.stderr)
                    ok = False
            if obj.get('task_set') == 'Constrained Policy Generation':
                if 'constraints' not in obj:
                    print(f'[L{i}] CPG missing constraints', file=sys.stderr)
                    ok = False
    if not ok:
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: validate_tasks.py tasks.jsonl')
        sys.exit(2)
    main(sys.argv[1])
