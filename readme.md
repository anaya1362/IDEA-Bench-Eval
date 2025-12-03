# IDEA-Bench Evaluation Pipeline (Improved Version)

This project implements a simplified and improved version of the evaluation pipeline described in the **IDEA-Bench** paper (*“Evaluating Generative Images by Description Alignment”*).  
The goal is to compare the **original scoring method** with a more **reliable and stable** evaluation pipeline.

---

## Overview

IDEA-Bench evaluates generated images using binary (0/1) questions answered by a multimodal LLM (MLLM).

The original evaluation pipeline has two main issues:

1. **Fragile text parsing** – MLLMs often produce inconsistent formats that break regex extraction.  
2. **No stability measurement** – scores vary across runs, but the pipeline only averages them and does not expose this variability.

This project reproduces the old method and introduces a more robust alternative.

---

## Old Pipeline (Baseline)

- **3 evaluation runs**
- Free-form text answers (e.g., `Q1: 1`)
- **Regex-based parsing** (prone to failure if format changes)
- Scores **averaged** across runs
- **No measure of consistency** across runs

---

## New Pipeline (Improved)

- **5 evaluation runs**
- **Strict JSON-only outputs** enforced (e.g., `{"Q1": 0, "Q2": 1, ...}`)
- **Retry mechanism** for invalid or non-JSON responses
- **Majority vote** instead of averaging per question
- A **consistency metric** showing how often the MLLM agrees with itself across runs

This design reduces parsing failures and produces clearer, more stable scores.

---

## Project Structure

```text
parser.py            # Old and new evaluators, JSON parsing, mock mode
evaluation_old.py    # Baseline regex-based evaluation
evaluation_new.py    # JSON-based improved evaluation
aggregator.py        # Aggregates scores and consistency
run_experiment.py    # Runs both pipelines and prints comparisons
