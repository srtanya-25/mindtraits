from rest_framework import serializers
from .models import Question, UserResponse, PersonalityResult


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'trait', 'order']


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['id', 'question', 'score', 'response_time_ms']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        # Upsert: update if answer already exists
        obj, _ = UserResponse.objects.update_or_create(
            user=validated_data['user'],
            question=validated_data['question'],
            defaults={
                'score': validated_data['score'],
                'response_time_ms': validated_data.get('response_time_ms', 0),
            }
        )
        return obj


class BulkResponseSerializer(serializers.Serializer):
    """Submit all answers in one shot: [{question: id, score: 1-5, response_time_ms: ms}]"""
    responses = UserResponseSerializer(many=True)


class PersonalityResultSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PersonalityResult
        fields = [
            'id', 'username',
            'openness', 'conscientiousness', 'extraversion',
            'agreeableness', 'neuroticism',
            'predicted_type', 'thinking_style',
            'career_recommendations', 'shap_explanation',
            'avg_response_time', 'created_at',
        ]
        read_only_fields = fields
