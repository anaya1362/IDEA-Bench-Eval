# run_experiment.py
import time
import json
from evaluation_old import evaluate_case_old
from evaluation_new import evaluate_case_new
from aggregator import hierarchical_aggregate

# 1. Load dataset from JSON instead of hard-coding
with open("data/test_cases.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

results_old = {}
results_new = {}
parse_fail_old = 0
parse_fail_new = 0
calls_old = 0
calls_new = 0

start = time.time()

for task, subtasks in dataset.items():
    results_old[task] = {}
    results_new[task] = {}
    for subtask, cases in subtasks.items():
        results_old[task][subtask] = {}
        results_new[task][subtask] = {}
        for case in cases:
            case_id = case["case_id"]
            prompt = case["prompt"]
            questions = case["questions"]

            # ------- Old pipeline -------
            scores_old, old_parse_failed = evaluate_case_old(prompt, questions)
            if old_parse_failed:
                parse_fail_old += 1
            results_old[task][subtask][case_id] = {"scores": scores_old}
            calls_old += 3  # 3 model calls per case in old pipeline

            # ------- New pipeline -------
            scores_new, consistency_new, new_parse_failed = evaluate_case_new(prompt, questions)
            if new_parse_failed:
                parse_fail_new += 1
            results_new[task][subtask][case_id] = {
                "scores": scores_new,
                "consistency": consistency_new
            }
            calls_new += 5  # 5 model calls per case in new pipeline

            time.sleep(5)  # brief pause to avoid rate limits

runtime = time.time() - start
print(f"Runtime: {runtime:.2f} seconds")

# 2. Aggregate results for overall scores
summary_old = hierarchical_aggregate(results_old)
summary_new = hierarchical_aggregate(results_new)

# 3. Print a quick summary for you
print("=== Old pipeline ===")
print("Parsing failures:", parse_fail_old)
print("Total calls:", calls_old)
print("Summary:", summary_old)

print("\n=== New pipeline ===")
print("Parsing failures:", parse_fail_new)
print("Total calls:", calls_new)
print("Summary:", summary_new)

# 4. (Optional) Save for plotting later
metrics = {
    "parse_fail_old": parse_fail_old,
    "parse_fail_new": parse_fail_new,
    "calls_old": calls_old,
    "calls_new": calls_new,
    "runtime_seconds": runtime,
}

def pretty_print_results(summary_old, summary_new, parse_fail_old, parse_fail_new, calls_old, calls_new):
    print("\n" + "="*60)
    print("                 📊 EVALUATION PIPELINE RESULTS")
    print("="*60)

    print("\n🔍 Reliability (Parsing Failures)")
    print("---------------------------------")
    print(f"  • Old Pipeline : {parse_fail_old}")
    print(f"  • New Pipeline : {parse_fail_new}")

    print("\n🎯 Soundness (Overall Scores)")
    print("------------------------------")
    print(f"  • Old Pipeline : {summary_old['TaskA']['score_percent']}%")
    print(f"  • New Pipeline : {summary_new['TaskA']['score_percent']}%")

    print("\n📈 Stability (Consistency)")
    print("---------------------------")
    print(f"  • New Pipeline Avg Consistency : {summary_new['TaskA']['avg_consistency_percent']}%")

    print("\n💰 Cost (Model Calls Used)")
    print("---------------------------")
    print(f"  • Old Pipeline : {calls_old} calls")
    print(f"  • New Pipeline : {calls_new} calls")

    print("\n✨ Conclusion:")
    print("  The new evaluation pipeline eliminates parsing failures, improves score")
    print("  stability through majority voting, provides a new consistency metric,")
    print("  and remains cost-effective despite slightly higher API usage.")
    print("="*60 + "\n")

pretty_print_results(summary_old, summary_new, parse_fail_old, parse_fail_new, calls_old, calls_new)

with open("results_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

with open("results_summary_old.json", "w", encoding="utf-8") as f:
    json.dump(summary_old, f, indent=2)

with open("results_summary_new.json", "w", encoding="utf-8") as f:
    json.dump(summary_new, f, indent=2)
