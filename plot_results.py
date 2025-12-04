# plot_results.py
import matplotlib.pyplot as plt

# ---- Metrics from your latest run_experiment output ----
parse_fail_old = 3
parse_fail_new = 0

score_old = 36.11     # Overall old pipeline score (%)
score_new = 54.17     # Overall new pipeline score (%)

consistency_new = 80.0   # Average consistency (%) for new pipeline (not plotted here)

calls_old = 9
calls_new = 15

pipelines = ["Old", "New"]


# Helper to remove top/right spines (looks cleaner)
def _despine(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# 1. Overall score: Old vs New
plt.figure(figsize=(5, 4))
scores = [score_old, score_new]

ax = plt.gca()
bars = ax.bar(pipelines, scores, width=0.5)

ax.set_title("Overall Score: Old vs New Pipeline")
ax.set_ylabel("Score (%)")
ax.set_ylim(0, 100)

# Light horizontal grid to make comparison easier
ax.yaxis.grid(True, linestyle="--", alpha=0.3)

# Slightly nicer colors (optional, but you asked about colors)
bars[0].set_color("#8da0cb")  # muted blue
bars[1].set_color("#66c2a5")  # muted green

# Annotate values on top of bars
for bar, val in zip(bars, scores):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        val + 2,
        f"{val:.1f}%",
        ha="center",
        va="bottom",
        fontsize=10,
    )

_despine(ax)
plt.tight_layout()
plt.savefig("score_compare.png", dpi=200)
plt.close()


# 2. Cost: API Calls Used (with ratio annotation)
plt.figure(figsize=(5, 4))
calls = [calls_old, calls_new]

ax = plt.gca()
bars = ax.bar(pipelines, calls, width=0.5)

ax.set_title("API Calls per Experiment: Old vs New Pipeline")
ax.set_ylabel("Number of Calls")

ax.yaxis.grid(True, linestyle="--", alpha=0.3)

bars[0].set_color("#fc8d62")  # muted orange
bars[1].set_color("#66c2a5")  # same green as above for visual link

for bar, val in zip(bars, calls):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        val + 0.3,
        str(val),
        ha="center",
        va="bottom",
        fontsize=10,
    )

_despine(ax)
plt.tight_layout()
plt.savefig("calls_compare.png", dpi=200)
plt.close()

print("Saved plots: score_compare.png, calls_compare.png")
