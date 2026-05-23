"""
insights/response_analytics.py
Computes behavioral analytics from response-time data.
"""

TRAIT_NAMES = {
    'O': 'Openness',
    'C': 'Conscientiousness',
    'E': 'Extraversion',
    'A': 'Agreeableness',
    'N': 'Neuroticism',
}


def compute_avg_response_times(responses_qs) -> dict:
    """
    Args:
        responses_qs: QuerySet of UserResponse objects
    Returns:
        {'Openness': avg_ms, 'Conscientiousness': avg_ms, ...}
    """
    trait_times: dict[str, list] = {t: [] for t in TRAIT_NAMES}

    for resp in responses_qs:
        trait_key = resp.question.trait
        if resp.response_time_ms > 0:
            trait_times[trait_key].append(resp.response_time_ms)

    result = {}
    for key, full_name in TRAIT_NAMES.items():
        times = trait_times[key]
        result[full_name] = round(sum(times) / len(times)) if times else 0

    return result


def behavioral_insights(avg_times: dict) -> str:
    """Returns a one-sentence behavioral insight based on slowest/fastest trait."""
    if not any(avg_times.values()):
        return "Complete the questionnaire to unlock behavioral insights."

    slowest = max(avg_times, key=avg_times.get)
    fastest = min(avg_times, key=avg_times.get)

    return (
        f"You deliberated most on {slowest} questions "
        f"(avg {avg_times[slowest]}ms) and responded fastest to "
        f"{fastest} questions (avg {avg_times[fastest]}ms), "
        f"suggesting deeper engagement with {slowest}-related thinking."
    )
