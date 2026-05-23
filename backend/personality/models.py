from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    TRAIT_CHOICES = [
        ('O', 'Openness'),
        ('C', 'Conscientiousness'),
        ('E', 'Extraversion'),
        ('A', 'Agreeableness'),
        ('N', 'Neuroticism'),
    ]

    text = models.TextField()
    trait = models.CharField(max_length=1, choices=TRAIT_CHOICES)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.text


class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField()                      # 1-5 Likert scale
    response_time_ms = models.PositiveIntegerField(default=0)  # milliseconds to answer
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} - {self.question.trait} ({self.score})"


class PersonalityResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')

    # Big Five raw scores
    openness = models.FloatField()
    conscientiousness = models.FloatField()
    extraversion = models.FloatField()
    agreeableness = models.FloatField()
    neuroticism = models.FloatField()

    # ML prediction label
    predicted_type = models.CharField(max_length=100, blank=True)

    # Thinking style (derived)
    thinking_style = models.CharField(max_length=100, blank=True)

    # Career recommendations (JSON list stored as text)
    career_recommendations = models.JSONField(default=list)

    # SHAP explanation
    shap_explanation = models.JSONField(default=dict)

    # Avg response times per trait
    avg_response_time = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.predicted_type} ({self.created_at.date()})"
