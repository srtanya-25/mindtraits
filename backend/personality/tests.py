"""
personality/tests.py
Tests for Question/UserResponse/PersonalityResult models and
the analysis pipeline (services.run_analysis_pipeline).
Pattern: TestCase + setUp() + targeted assertions.
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ValidationError

from personality.models import Question, UserResponse, PersonalityResult
from personality.services import compute_scores, run_analysis_pipeline


class QuestionModelTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            text="I enjoy thinking about abstract ideas", trait="O", order=1
        )

    def test_question_creation(self):
        self.assertEqual(self.question.trait, "O")
        self.assertEqual(self.question.order, 1)

    def test_trait_max_length_is_one(self):
        max_length = self.question._meta.get_field("trait").max_length
        self.assertEqual(max_length, 1)

    def test_invalid_trait_choice_fails_clean(self):
        invalid = Question(text="Bad trait code", trait="Z", order=2)
        with self.assertRaises(ValidationError):
            invalid.full_clean()


class ComputeScoresTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="erin", password="test12345")
        # one question per trait
        traits = ["O", "C", "E", "A", "N"]
        for i, t in enumerate(traits, start=1):
            q = Question.objects.create(text=f"Q{i}", trait=t, order=i)
            UserResponse.objects.create(user=self.user, question=q, score=4, response_time_ms=1500)

    def test_compute_scores_sums_by_trait(self):
        responses = UserResponse.objects.filter(user=self.user).select_related("question")
        scores = compute_scores(responses)
        self.assertEqual(scores, {"O": 4, "C": 4, "E": 4, "A": 4, "N": 4})


class AnalysisPipelineTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="finn", password="test12345")
        for i, t in enumerate(["O", "C", "E", "A", "N"], start=1):
            q = Question.objects.create(text=f"Q{i}", trait=t, order=i)
            UserResponse.objects.create(user=self.user, question=q, score=5, response_time_ms=2000)

    def test_pipeline_creates_result(self):
        result = run_analysis_pipeline(self.user)
        self.assertIsInstance(result, PersonalityResult)
        self.assertEqual(result.user, self.user)
        self.assertTrue(result.predicted_type)              # fallback label exists
        self.assertTrue(result.thinking_style)              # mapping returns something
        self.assertIsInstance(result.career_recommendations, list)
        self.assertGreater(len(result.career_recommendations), 0)

    def test_pipeline_raises_without_responses(self):
        empty_user = User.objects.create_user(username="ghost", password="test12345")
        with self.assertRaises(ValueError):
            run_analysis_pipeline(empty_user)
