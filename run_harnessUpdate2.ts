// run_harness.ts — TypeScript reference harness
import * as fs from 'fs';
import * as path from 'path';

interface Task {
  id: string;
  task_set: string;
  [key: string]: any;
}

function loadTasks(filePath: string): Task[] {
  return fs.readFileSync(filePath, 'utf-8')
    .split('\n')
    .filter(Boolean)
    .map(line => JSON.parse(line));
}

function simulateModelCall(task: Task): { output: string, trace: string } {
  if (task.task_set === 'Adversarial Fact Verification') {
    return { output: `Answer: ${task.ground_truth}`, trace: 'Selected authoritative source.' };
  } else if (task.task_set === 'Multi-Step Tool-Augmented Reasoning') {
    return { output: JSON.stringify(task.ground_truth), trace: 'Computed from structured data.' };
  } else {
    return { output: 'Policy response within constraints.', trace: 'Checked against constraints.' };
  }
}

function main() {
  const tasks = loadTasks('tasks.jsonl');
  const results: any[] = [];
  for (const t of tasks) {
    const r = simulateModelCall(t);
    results.push({ id: t.id, task_set: t.task_set, output: r.output, trace: r.trace });
  }
  fs.writeFileSync('results.jsonl', results.map(r => JSON.stringify(r)).join('\n'));
  console.log('Wrote results.jsonl');
}

main();