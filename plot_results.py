# plot_results.py
import matplotlib.pyplot as plt

# Example data from experiment (these would come from run_experiment output)
parse_fail_old = 5
parse_fail_new = 0
calls_old = 300
calls_new = 500
scores_old = [35.5, 60.0, 45.5, 50.0]  # sample subtask scores (percent)
scores_new = [33.3, 61.1, 44.4, 55.6]  # sample corresponding scores from new pipeline

# 1. Parsing failure rate bar chart
plt.figure(figsize=(4,3))
plt.bar(["Old Pipeline", "New Pipeline"], [parse_fail_old, parse_fail_new], color=['#d62728','#2ca02c'])
plt.title("Parsing Failures: Old vs New Pipeline")
plt.ylabel("Number of Failed Parses")
plt.savefig("parse_fail_compare.png")

# 2. Score comparison scatter
plt.figure(figsize=(4,4))
plt.scatter(scores_old, scores_new, c='blue')
plt.plot([0,100], [0,100], '--', color='gray')  # reference line y=x
plt.xlabel("Old Pipeline Score (%)")
plt.ylabel("New Pipeline Score (%)")
plt.title("Subtask Score Comparison")
plt.savefig("score_comparison.png")
