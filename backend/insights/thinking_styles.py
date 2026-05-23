"""
insights/thinking_styles.py
Maps Big Five trait scores to a dominant thinking style label.
"""

THINKING_STYLE_MAP = [
    # (condition_fn, label, description)
    (lambda s: s['O'] >= 16 and s['E'] >= 14, "Visionary Thinker",
     "You think in big pictures, love brainstorming and thrive in dynamic environments."),

    (lambda s: s['C'] >= 16 and s['A'] >= 14, "Systematic Planner",
     "You approach problems methodically, plan ahead and value reliability."),

    (lambda s: s['E'] >= 16 and s['A'] >= 14, "Collaborative Connector",
     "You process ideas best through discussion and build strong relationship networks."),

    (lambda s: s['N'] >= 14 and s['O'] >= 14, "Reflective Analyst",
     "You think deeply, notice nuance and bring careful introspection to decisions."),

    (lambda s: s['C'] >= 16 and s['N'] <= 10, "Focused Executor",
     "You cut through complexity, stay calm under pressure and deliver results."),

    (lambda s: s['A'] >= 16, "Empathetic Mediator",
     "You lead with empathy, excel at consensus-building and value harmony."),

    (lambda s: True, "Balanced Thinker",
     "You adapt flexibly across different situations with a well-rounded cognitive style."),
]


def get_thinking_style(scores: dict) -> dict:
    """
    Args:
        scores: {'O': float, 'C': float, 'E': float, 'A': float, 'N': float}
    Returns:
        {'label': str, 'description': str}
    """
    for condition, label, description in THINKING_STYLE_MAP:
        if condition(scores):
            return {"label": label, "description": description}
    return {"label": "Balanced Thinker", "description": ""}
