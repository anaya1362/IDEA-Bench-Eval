# aggregator.py
import numpy as np

def aggregate_task_results(results_by_case: dict):
    """
    Given a dict of {case_id: {'scores': [q1,...,q6], 'consistency': [c1,...,c6]}} for a subtask or task,
    return aggregated score and consistency.
    """
    all_scores = []
    all_consistency = []
    for case_id, data in results_by_case.items():
        scores = data['scores']  # list of 0/1 (new) or fractional (old) scores per question
        cons = data.get('consistency', [1]*len(scores))  # consistency list (for old pipeline, assume 1 for binary outputs)
        all_scores.extend(scores)
        all_consistency.extend(cons)
    # Calculate percentage of questions answered correctly in this set
    avg_score = np.mean(all_scores)  # fraction of questions scored 1 (or average if fractional old scores)
    percent_score = avg_score * 100  # percentage form
    # Overall consistency: we use average consistency across all questions (only meaningful for new pipeline)
    avg_consistency = np.mean(all_consistency) * 100
    return percent_score, avg_consistency

def hierarchical_aggregate(all_results: dict):
    """
    Aggregate results at subtask and task level.
    all_results is structured as {task: {subtask: {case: {...}}}}.
    Returns a structure with aggregated scores per subtask and per task.
    """
    task_summary = {}
    for task, subtasks in all_results.items():
        task_scores = []
        task_consistency = []
        subtask_summary = {}
        for subtask, cases in subtasks.items():
            subtask_score, subtask_consist = aggregate_task_results(cases)
            subtask_summary[subtask] = {
                "score_percent": round(subtask_score, 2),
                "avg_consistency_percent": round(subtask_consist, 2)
            }
            task_scores.append(subtask_score)
            task_consistency.append(subtask_consist)
        # Average across subtasks for overall task category score
        task_score = np.mean(task_scores)
        task_consist = np.mean(task_consistency) if task_consistency else 0
        task_summary[task] = {
            "subtasks": subtask_summary,
            "score_percent": round(task_score, 2),
            "avg_consistency_percent": round(task_consist, 2)
        }
    return task_summary
