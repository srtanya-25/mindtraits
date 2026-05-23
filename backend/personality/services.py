"""
personality/services.py
Orchestrates: score aggregation → ML prediction → thinking style → career insights → SHAP
"""
from .models import UserResponse, PersonalityResult
from insights.thinking_styles import get_thinking_style
from insights.career_mapping import get_career_recommendations
from insights.response_analytics import compute_avg_response_times
from ml_models.predict import predict_personality


def compute_scores(responses_qs) -> dict:
    """Aggregate raw Big Five scores from UserResponse queryset."""
    scores = {'O': 0, 'C': 0, 'E': 0, 'A': 0, 'N': 0}
    for resp in responses_qs:
        scores[resp.question.trait] += resp.score
    return scores


def run_analysis_pipeline(user) -> PersonalityResult:
    """
    Full pipeline for a user after submitting all answers.
    Returns a saved PersonalityResult instance.
    """
    responses = UserResponse.objects.filter(user=user).select_related('question')

    if not responses.exists():
        raise ValueError("No responses found for user.")

    # 1. Score aggregation
    scores = compute_scores(responses)

    # 2. Response-time analytics
    avg_times = compute_avg_response_times(responses)

    # 3. ML prediction + SHAP
    ml_result = predict_personality(scores)
    predicted_type = ml_result['predicted_type']
    shap_explanation = ml_result['shap_explanation']

    # 4. Thinking style
    thinking = get_thinking_style(scores)

    # 5. Career recommendations
    careers = get_career_recommendations(predicted_type)

    # 6. Save result (latest replaces previous for this user)
    result, _ = PersonalityResult.objects.update_or_create(
        user=user,
        defaults={
            'openness': scores['O'],
            'conscientiousness': scores['C'],
            'extraversion': scores['E'],
            'agreeableness': scores['A'],
            'neuroticism': scores['N'],
            'predicted_type': predicted_type,
            'thinking_style': thinking['label'],
            'career_recommendations': careers,
            'shap_explanation': shap_explanation,
            'avg_response_time': avg_times,
        }
    )

    return result
