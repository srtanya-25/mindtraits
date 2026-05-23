"""
api/tests.py
Smoke tests for the api aggregator endpoints.
"""
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from personality.models import Question


class QuestionListEndpointTest(TestCase):
    """GET /api/v1/questions/ is public and returns the seeded questions."""

    def setUp(self):
        self.client = APIClient()
        Question.objects.create(text="I have many creative ideas", trait="O", order=1)
        Question.objects.create(text="I pay attention to details", trait="C", order=2)

    def test_questions_endpoint_is_public(self):
        response = self.client.get("/api/v1/questions/")
        self.assertEqual(response.status_code, 200)

    def test_questions_returns_seeded_data(self):
        response = self.client.get("/api/v1/questions/")
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 2)


class AuthFlowTest(TestCase):
    """Register → dashboard auth check round-trip."""

    def setUp(self):
        self.client = APIClient()

    def test_register_creates_user(self):
        response = self.client.post(
            "/api/v1/register/",
            {"username": "rathalu", "email": "r@example.com", "password": "test12345"},
            format="json",
        )
        self.assertIn(response.status_code, (200, 201))
        self.assertTrue(User.objects.filter(username="rathalu").exists())

    def test_dashboard_requires_authentication(self):
        response = self.client.get("/api/v1/dashboard-protected/")
        # CookieJWTAuthentication returns None (no cookie) → IsAuthenticated fails → 401
        self.assertEqual(response.status_code, 401)
