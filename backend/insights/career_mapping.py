"""
insights/career_mapping.py
Maps Big Five personality scores to career recommendations.
"""

CAREER_MAP = {
    'Creative Explorer': [
        "UX/UI Designer", "Creative Director", "Product Innovator",
        "Architect", "Film Director", "Game Designer",
    ],
    'Organized Achiever': [
        "Project Manager", "Data Analyst", "Financial Planner",
        "Software Engineer", "Operations Manager", "Accountant",
    ],
    'Social Dynamo': [
        "Marketing Manager", "Sales Executive", "Public Relations Specialist",
        "HR Manager", "Event Coordinator", "Business Development",
    ],
    'Empathetic Helper': [
        "Counselor / Therapist", "Social Worker", "Nurse / Doctor",
        "Teacher / Educator", "Nonprofit Manager", "Community Organizer",
    ],
    'Sensitive Thinker': [
        "Research Scientist", "Writer / Journalist", "Philosopher",
        "Clinical Psychologist", "Data Scientist", "Literature / Arts",
    ],
    'Balanced Personality': [
        "Entrepreneur", "Consultant", "General Manager",
        "Product Manager", "Business Analyst",
    ],
}


def get_career_recommendations(predicted_type: str) -> list:
    return CAREER_MAP.get(predicted_type, CAREER_MAP['Balanced Personality'])
