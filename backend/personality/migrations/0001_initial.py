# Generated for MindTraits — initial migration
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                ("trait", models.CharField(choices=[("O", "Openness"), ("C", "Conscientiousness"), ("E", "Extraversion"), ("A", "Agreeableness"), ("N", "Neuroticism")], max_length=1)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="UserResponse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.IntegerField()),
                ("response_time_ms", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="personality.question")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="responses", to=settings.AUTH_USER_MODEL)),
            ],
            options={"unique_together": {("user", "question")}},
        ),
        migrations.CreateModel(
            name="PersonalityResult",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("openness", models.FloatField()),
                ("conscientiousness", models.FloatField()),
                ("extraversion", models.FloatField()),
                ("agreeableness", models.FloatField()),
                ("neuroticism", models.FloatField()),
                ("predicted_type", models.CharField(blank=True, max_length=100)),
                ("thinking_style", models.CharField(blank=True, max_length=100)),
                ("career_recommendations", models.JSONField(default=list)),
                ("shap_explanation", models.JSONField(default=dict)),
                ("avg_response_time", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="results", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
