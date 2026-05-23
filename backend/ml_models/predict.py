"""
ml_models/predict.py
Loads the trained XGBoost model and runs personality prediction + SHAP explanation.
Falls back to rule-based scoring when model.pkl is not yet trained.
"""
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def _rule_based_label(scores: dict) -> str:
    """Simple rule-based label used as fallback before ML model is trained."""
    dominant = max(scores, key=scores.get)
    labels = {
        'O': 'Creative Explorer',
        'C': 'Organized Achiever',
        'E': 'Social Dynamo',
        'A': 'Empathetic Helper',
        'N': 'Sensitive Thinker',
    }
    return labels.get(dominant, 'Balanced Personality')


def predict_personality(scores: dict) -> dict:
    """
    Args:
        scores: {'O': float, 'C': float, 'E': float, 'A': float, 'N': float}
    Returns:
        {
            'predicted_type': str,
            'shap_explanation': dict   # feature -> impact_percent
        }
    """
    feature_vector = np.array([[
        scores['O'], scores['C'], scores['E'], scores['A'], scores['N']
    ]], dtype=float)

    try:
        import pickle
        import shap

        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)

        predicted_label = model.predict(feature_vector)[0]

        # SHAP explanation
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(feature_vector)

        trait_names = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
        total = sum(abs(v) for v in shap_values[0]) or 1
        shap_explanation = {
            trait: round(abs(val) / total * 100, 1)
            for trait, val in zip(trait_names, shap_values[0])
        }

        return {"predicted_type": str(predicted_label), "shap_explanation": shap_explanation}

    except Exception:
        # Fallback: no trained model yet
        label = _rule_based_label(scores)
        total = sum(scores.values()) or 1
        shap_explanation = {
            'Openness': round(scores['O'] / total * 100, 1),
            'Conscientiousness': round(scores['C'] / total * 100, 1),
            'Extraversion': round(scores['E'] / total * 100, 1),
            'Agreeableness': round(scores['A'] / total * 100, 1),
            'Neuroticism': round(scores['N'] / total * 100, 1),
        }
        return {"predicted_type": label, "shap_explanation": shap_explanation}
