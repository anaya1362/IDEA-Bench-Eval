# evaluation_old.py
import re
import numpy as np
from parser import mllm_evaluate_old, USE_MOCK

# Use 3 runs in mock mode (for experiments), fewer runs with real API
NUM_RUNS_OLD = 3 if USE_MOCK else 1


def evaluate_case_old(case_prompt: str, questions: list[str]):
    """
    OLD PIPELINE:
    - Runs 3 times
    - Fragile regex parsing
    - Returns (avg_scores, parse_failed)
    """
    runs = []
    parse_failed = False

    for _ in range(NUM_RUNS_OLD):
        full_prompt = case_prompt + "\n" + "\n".join(questions)
        response = mllm_evaluate_old(full_prompt)

        scores = []
        for i, q in enumerate(questions, start=1):
            # Try to capture "Q1: 1" or "Q1 = 0" patterns
            match = re.search(fr"Q{i}\s*[:=]\s*([01])", response)

            if match:
                scores.append(int(match.group(1)))
            else:
                # Regex could not find answer → parsing failed
                scores.append(0)
                parse_failed = True   # mark failure for this run/question

        runs.append(scores)

    runs_array = np.array(runs)
    avg_scores = runs_array.mean(axis=0).tolist()

    return avg_scores, parse_failed
