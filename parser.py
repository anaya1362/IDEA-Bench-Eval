# parser.py
import os
import json
import re
import random
from google import genai

# Set to False only when you really want to hit the Gemini API.
USE_MOCK = True
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# ---------- OLD PIPELINE: text-style, fragile for regex ----------
def mllm_evaluate_old(prompt: str) -> str:
    """
    Old-style evaluator:
    - Returns free-form text like 'Q1: 1', 'Q2: 0', sometimes messy.
    - This is what the regex parser in evaluation_old.py tries to handle.
    """
    if USE_MOCK or not client.api_key:
        lines = []
        for i in range(1, 7):
            val = 1 if i % 2 == 0 else 0  # base pattern
            # Sometimes break the expected 'Qk: 0/1' format to simulate parse failures.
            if random.random() < 0.3:
                txt = "Yes" if val == 1 else "No"
                lines.append(f"Question {i}: {txt}")  # regex will NOT match this
            else:
                lines.append(f"Q{i}: {val}")          # regex will match this
        lines.append("Overall this design looks okay.")
        return "\n".join(lines)

    # Real Gemini call: ask for 'Qk: 0' style answers.
    resp = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            prompt
            + "\nFor each question Q1..Q6, answer on a new line as 'Qk: 0' or 'Qk: 1'."
        ),
    )
    return resp.text


# ---------- NEW PIPELINE: JSON-style, robust parsing ----------
def mllm_evaluate_new(prompt: str) -> str:
    """
    New-style evaluator:
    - Should return ONLY JSON like {"Q1": 0, "Q2": 1, ...}.
    - This is what parse_response() expects.
    """
    if USE_MOCK or not client.api_key:
        # Mock: random but valid 0/1 answers.
        answers = {}
        for i in range(1, 7):
            base = 1 if i % 2 == 0 else 0
            # Small chance of flipping to create inconsistency across runs.
            if random.random() < 0.2:
                base = 1 - base
            answers[f"Q{i}"] = base
        return json.dumps(answers)

    resp = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            prompt
            + '\nReturn ONLY JSON like {"Q1": 0, "Q2": 1, ...}. Do not add extra text.'
        ),
    )
    return resp.text


def _extract_json_block(text: str) -> str:
    """Extract the first {...} block from text, stripping ```json fences if present."""
    text = re.sub(r"```(?:json)?", "", text).strip()
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        raise json.JSONDecodeError("No JSON object found", text, 0)
    return m.group(0)


def parse_response(question_prompt: str, max_retries: int = 2):
    """
    New pipeline JSON parser:
    - Calls mllm_evaluate_new
    - Tries to parse JSON; on failure, edits prompt and retries.
    - Raises ValueError if all attempts fail.
    """
    attempt = 0
    while attempt <= max_retries:
        response_text = mllm_evaluate_new(question_prompt)
        try:
            json_str = _extract_json_block(response_text)
            result = json.loads(json_str)
            if isinstance(result, dict) and all(k.startswith("Q") for k in result.keys()):
                return result
        except (json.JSONDecodeError, TypeError):
            pass

        attempt += 1
        if attempt <= max_retries:
            question_prompt += "\nRemember: Output only JSON with numeric 0/1 values."

    raise ValueError("Failed to parse MLLM response as JSON after retries.")
