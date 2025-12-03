IDEA-Bench Evaluation Pipeline (Improved Version)

This project implements a simplified and improved version of the evaluation pipeline described in the IDEA-Bench paper (“Evaluating Generative Images by Description Alignment”).
The goal is to compare the original scoring method with a more reliable and stable evaluation pipeline.

Overview

IDEA-Bench evaluates generated images using binary (0/1) questions answered by an MLLM.
The original evaluation pipeline has two issues:

Fragile text parsing – MLLMs often produce inconsistent formats that break regex extraction.

No stability measurement – scores vary across runs, but the pipeline only averages them.

This project reproduces the old method and introduces a more robust alternative.

Old Pipeline (Baseline)

3 evaluation runs

Free-form text answers (e.g., “Q1: 1”)

Regex-based parsing (prone to failure)

Scores averaged across runs

No measure of consistency

New Pipeline (Improved)

5 evaluation runs

Strict JSON-only outputs enforced

Retry mechanism for invalid responses

Majority vote instead of averaging

A consistency metric showing how often the MLLM agrees with itself

This design reduces parsing failures and gives a clearer, more stable score.

Project Structure
parser.py            # Old and new evaluators, JSON parsing, mock mode
evaluation_old.py    # Baseline regex-based evaluation
evaluation_new.py    # JSON-based improved evaluation
aggregator.py        # Aggregates scores and consistency
run_experiment.py    # Runs both pipelines and prints comparisons

Running the Code

Inside the project folder:

python run_experiment.py


By default, the project uses mock mode to avoid rate limits.
To use Gemini, set your API key and disable mock mode in parser.py.

Summary of Findings

The old pipeline frequently fails to parse and produces unstable averages.

The new pipeline eliminates parsing failures, produces clean binary scores, and adds a consistency measure.

This aligns with reliability improvements proposed in the project slides.