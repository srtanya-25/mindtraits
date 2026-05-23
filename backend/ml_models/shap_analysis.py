"""
ml_models/shap_analysis.py
Standalone SHAP utilities — separated from predict.py so the explainability
logic can be unit-tested or swapped without touching the prediction path.
"""
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

TRAIT_NAMES = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]


def explain_prediction(feature_vector):
    """
    Args:
        feature_vector: numpy array of shape (1, 5)  — [O, C, E, A, N]

    Returns:
        dict: {trait_name: impact_percent}  — how much each trait
              drove the model's prediction (absolute SHAP value, normalised to 100%).

        Returns an empty dict if the model or shap library isn't available
        (the rule-based fallback in predict.py will be used instead).
    """
    try:
        import pickle
        import shap
    except ImportError:
        return {}

    if not os.path.exists(MODEL_PATH):
        return {}

    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(feature_vector)

        # For multi-class, shap_values is a list of arrays — pick the predicted class
        if isinstance(shap_values, list):
            predicted_class_idx = int(model.predict(feature_vector)[0])
            class_shap = shap_values[predicted_class_idx][0]
        else:
            class_shap = shap_values[0]

        total = sum(abs(v) for v in class_shap) or 1
        return {trait: round(abs(val) / total * 100, 1) for trait, val in zip(TRAIT_NAMES, class_shap)}

    except Exception:
        return {}


def rule_based_explanation(scores: dict) -> dict:
    """Score-proportional explanation used when the ML model is not yet trained."""
    total = sum(scores.values()) or 1
    return {
        "Openness":          round(scores["O"] / total * 100, 1),
        "Conscientiousness": round(scores["C"] / total * 100, 1),
        "Extraversion":      round(scores["E"] / total * 100, 1),
        "Agreeableness":     round(scores["A"] / total * 100, 1),
        "Neuroticism":       round(scores["N"] / total * 100, 1),
    }
