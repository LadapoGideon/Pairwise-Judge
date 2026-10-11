"""Analyse pairwise preference judgments for position bias and consistency.

In a pairwise test, a judge sees two responses and picks A, B, or tie.
Judges often favour whichever response is shown first. Swapping the order
and checking whether the verdict follows the response (not the position)
is a standard way to catch this.
"""
from collections import Counter


def map_to_model(position_verdict, shown_as):
    """
    position_verdict: "A", "B", or "tie" as the judge answered.
    shown_as: (model shown as A, model shown as B).
    Returns the model name the judge preferred, or "tie".
    """
    if position_verdict == "tie":
        return "tie"
    if position_verdict == "A":
        return shown_as[0]
    if position_verdict == "B":
        return shown_as[1]
    raise ValueError(f"unknown verdict {position_verdict!r}")


def position_bias(position_verdicts):
    """Share of decisive verdicts that picked position A. 0.5 means no bias."""
    decisive = [v for v in position_verdicts if v in ("A", "B")]
    if not decisive:
        raise ValueError("no decisive verdicts")
    return sum(1 for v in decisive if v == "A") / len(decisive)


def swap_consistency(pairs):
    """
    pairs: list of (model_preferred_in_original_order, model_preferred_after_swap).
    Returns the share of prompts where the judge picked the same model both times.
    """
    if not pairs:
        raise ValueError("no pairs")
    same = sum(1 for first, second in pairs if first == second)
    return same / len(pairs)


def win_rates(results):
    """
    results: list of winning model names, or "tie".
    Ties count as half a win for each side, so a model's rate can be compared fairly.
    Returns {model: rate} where rate is wins divided by total games it played.
    """
    counts = Counter(results)
    models = {m for m in counts if m != "tie"}
    total_games = len(results)
    if total_games == 0:
        raise ValueError("no results")
    # Each non-tie result is one game for the winner and one for the loser.
    # Simple version: count wins against all decided games in the list.
    rates = {}
    for model in models:
        wins = counts[model] + 0.5 * counts["tie"]
        rates[model] = round(wins / total_games, 4)
    return rates
