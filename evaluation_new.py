# evaluation_new.py
import numpy as np
from parser import parse_response, USE_MOCK

# Use 5 runs in mock mode, fewer with real API
NUM_RUNS_NEW = 5 if USE_MOCK else 2


def evaluate_case_new(case_prompt: str, questions: list[str]):
    """
    NEW PIPELINE:
    - Runs 5 times
    - Strict JSON parsing + retries
    - Majority vote scoring
    - Returns (final_scores, consistency, parse_failed)
    """
    runs = []
    parse_failed = False   # track if ANY of the 3 runs failed JSON parsing

    for _ in range(NUM_RUNS_NEW):
        full_prompt = case_prompt + "\nPlease answer the following questions with 0 or 1 in JSON format:\n"
        for i, q in enumerate(questions, start=1):
            full_prompt += f"Q{i}: {q}\n"

        try:
            result = parse_response(full_prompt)  # expected: {"Q1": 0, ..., "Q6": 1}
        except ValueError:
            # JSON parsing failed even after retries
            result = {}
            parse_failed = True

        # Extract answers or default to 0
        scores = [int(result.get(f"Q{i}", 0)) for i in range(1, len(questions)+1)]
        runs.append(scores)

    runs_array = np.array(runs)

    # ---- Majority Vote ----
    final_scores = []
    consistency = []
    for j in range(runs_array.shape[1]):
        answers = runs_array[:, j]
        ones = np.sum(answers)
        zeros = len(answers) - ones

        final = 1 if ones > zeros else 0
        final_scores.append(final)

        # consistency = fraction of runs matching majority
        agree_count = ones if final == 1 else zeros
        consistency.append(agree_count / len(answers))

    return final_scores, consistency, parse_failed
