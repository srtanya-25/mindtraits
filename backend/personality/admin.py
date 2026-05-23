from django.contrib import admin
from .models import Question, UserResponse, PersonalityResult


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'trait', 'text', 'order')
    list_filter = ('trait',)
    search_fields = ('text',)
    ordering = ('order', 'id')


@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'score', 'response_time_ms', 'created_at')
    list_filter = ('question__trait', 'created_at')
    search_fields = ('user__username',)


@admin.register(PersonalityResult)
class PersonalityResultAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'predicted_type', 'thinking_style',
        'openness', 'conscientiousness', 'extraversion',
        'agreeableness', 'neuroticism', 'created_at'
    )
    list_filter = ('predicted_type', 'thinking_style', 'created_at')
    search_fields = ('user__username',)
